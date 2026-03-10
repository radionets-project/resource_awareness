"""Adapted from radionets source code

https://github.com/radionets-project/radionets

Under the MIT License
"""

from pathlib import Path

import h5py
import numpy as np
import torch
from lightning import LightningDataModule
from natsort import natsorted
from torch.utils.data import DataLoader, Dataset


class H5DataSet(Dataset):
    def __init__(self, data_dir: Path, tar_fourier: bool, mode: str = "train"):
        """
        Save the bundle paths and the number of bundles in one file.
        """
        bundle_paths = data_dir.glob(f"samp_{mode}_*.h5")
        self.bundles = natsorted(bundle_paths)

        if not self.bundles:
            raise FileNotFoundError(
                f"No HDF5 files were found in {data_dir} for mode '{mode}'"
            )

        self.num_img = len(self.open_bundle(self.bundles[0], "x"))
        self.tar_fourier = tar_fourier

    def __call__(self):
        return print("This is the H5DataSet class.")

    def __len__(self):
        """
        Returns the total number of pictures in this dataset
        """
        return len(self.bundles) * self.num_img

    def __getitem__(self, i):  # ty:ignore[invalid-method-override]
        x = self.open_image("x", i)
        y = self.open_image("y", i)
        return x, y

    def open_bundle(self, bundle_path, var):
        bundle = h5py.File(bundle_path, "r")
        data = bundle[var]
        return data

    def open_image(self, var, i):
        if isinstance(i, int):
            i = torch.tensor([i])

        elif isinstance(i, np.ndarray):
            i = torch.tensor(i)

        indices, _ = torch.sort(i)
        bundle = torch.div(indices, self.num_img, rounding_mode="floor")
        image = indices - bundle * self.num_img
        bundle_unique = torch.unique(bundle)

        bundle_paths = [
            h5py.File(self.bundles[bundle], "r") for bundle in bundle_unique
        ]
        bundle_paths_str = list(map(str, bundle_paths))

        data = torch.from_numpy(
            np.array(
                [
                    bund[var][img]
                    for bund, bund_str in zip(bundle_paths, bundle_paths_str)
                    for img in image[
                        bundle == bundle_unique[bundle_paths_str.index(bund_str)]
                    ]
                ]
            )
        )

        if self.tar_fourier is False and data.shape[1] == 2:
            raise ValueError(
                "Two channeled data is used despite Fourier being False.\
                    Set Fourier to True!"
            )

        if data.shape[0] == 1:
            data = data.squeeze(0)
        return data.float()


class H5DataModule(LightningDataModule):
    """
    PyTorch Lightning DataModule for handling visibility
    data from HDF5 files.

    This DataModule manages the loading and preparation
    of the visibility datasets for training, validation,
    testing, and prediction stages of radionets.

    Parameters
    ----------
    data_dir : str or :class:`pathlib.Path`
        Directory path containing the HDF5 data files.
    batch_size : int, optional
        Number of samples per batch.
        Default: ``32``
    fourier : bool, optional
        Whether to use Fourier space targets.
        Default: ``False``
    num_workers : int, optional
        Number of worker processes for data loading.
        Default ``10``

    Attributes
    ----------
    fourier : bool
        Flag indicating whether Fourier space inputs/targets
        are used.
    data_dir : str or Path
        Directory path to the data.
    batch_size : int
        Batch size for data loaders.
    num_workers : int
        Number of worker processes.
    vis_train : H5DataSet
        Training dataset used in the Trainer.fit stage.
    vis_val : H5DataSet
        Validation dataset used in the Trainer.validate
        stage.
    vis_test : H5DataSet
        Test dataset used in the Trainer.test stage.
    vis_predict : H5DataSet
        Prediction dataset used for inference in the
        Trainer.predict stage.
    """

    def __init__(
        self,
        data_dir: str | Path,
        *,
        batch_size: int = 32,
        fourier: bool = True,
        num_workers: int = 10,
        **kwargs,
    ):
        super().__init__()
        self.fourier = fourier
        self.batch_size = batch_size
        self.num_workers = num_workers

        if not isinstance(data_dir, Path):
            data_dir = Path(data_dir)

        self.data_dir = data_dir.expanduser().resolve()

        self.save_hyperparameters()

    def setup(self, stage: str):
        """
        Set up datasets for the specified stage.

        Creates H5DataSet instances for the appropriate data
        splits based on the stage of the workflow
        (fit, test, or predict).

        Parameters
        ----------
        stage : str
            The stage of the workflow. Must be one of:

            - 'fit': Prepares training and validation datasets
            - 'test': Prepares test dataset
            - 'predict': Prepares prediction dataset

        Raises
        ------
        ValueError
            If the provided stage is not one of 'fit', 'test',
            or 'predict'.

        Notes
        -----
        This method is called automatically by PyTorch Lightning
        before any one of the training, validation, testing, or
        prediction loop begins.
        """
        match stage:
            case "fit":
                self.vis_train = H5DataSet(
                    self.data_dir,
                    tar_fourier=self.fourier,
                    mode="train",
                )
                self.vis_val = H5DataSet(
                    self.data_dir,
                    tar_fourier=self.fourier,
                    mode="valid",
                )

            case "test":
                self.vis_test = H5DataSet(
                    self.data_dir,
                    tar_fourier=self.fourier,
                    mode="test",
                )
            case "predict":
                self.vis_predict = H5DataSet(
                    self.data_dir,
                    tar_fourier=self.fourier,
                    mode="test",
                )
            case _:
                raise ValueError(
                    f"Stage {stage} is not available in {self.__class__.__name__}"
                )

    def train_dataloader(self):
        """
        Create and return the training DataLoader.

        Returns
        -------
        :class:`torch.utils.data.DataLoader`
            PyTorch DataLoader for the training dataset with
            configured batch size and number of workers.
        """
        return DataLoader(
            self.vis_train,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def val_dataloader(self):
        """
        Create and return the validation DataLoader.

        Returns
        -------
        :class:`torch.utils.data.DataLoader`
            PyTorch DataLoader for the validation dataset
            with configured batch size and number of workers.
        """
        return DataLoader(
            self.vis_val,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def test_dataloader(self):
        """
        Create and return the test DataLoader.

        Returns
        -------
        :class:`torch.utils.data.DataLoader`
            PyTorch DataLoader for the test dataset with
            configured batch size and number of workers.
        """
        return DataLoader(
            self.vis_test,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )

    def predict_dataloader(self):
        """
        Create and return the prediction DataLoader.

        Returns
        -------
        :class:`torch.utils.data.DataLoader`
            PyTorch DataLoader for the prediction dataset
            with configured batch size and number of workers.
        """
        return DataLoader(
            self.vis_predict,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
        )
