"""Adapted from radionets source code

https://github.com/radionets-project/radionets

Under the MIT License
"""

import numpy as np
import torch
import torch.nn.functional as F


def get_predictions(
    trainer, task="training"
) -> tuple[np.ndarray, np.ndarray] | np.ndarray:
    """Get the prediction of the model.

    Parameters
    ----------
    trainer : lightning.pytorch.trainer.trainer.Trainer
        Lightning Trainer instance used to train the model.
    task : str, optional
        Task to perform. Either 'training' or 'inference'. This
        will select the respective dataloader from the datamodule.
        Default: 'training'

    Returns
    -------
    ifft_preds : torch.Tensor
        Fourier transformed predictions.
    ifft_targets : torch.Tensor
        Fourier transformed targets. Targets are only returned
        if task is set to 'training'.
    """
    ifft_preds = []
    ifft_targets = []

    match task:
        case "inference":
            dataloader = trainer.datamodule.predict_dataloader()

            for batch in dataloader:
                preds = trainer.model.predict_step(batch[0], batch_idx=0).detach().cpu()

                # check if images are half or full
                if preds.shape[-2] != preds.shape[-1]:
                    preds = apply_symmetry(preds)

                ifft_preds.extend(get_ifft(preds))

            return torch.stack(ifft_preds).detach().cpu().numpy()

        case "training":
            dataloader = trainer.datamodule.val_dataloader()

            for batch in dataloader:
                preds = trainer.model.predict_step(batch[0], batch_idx=0).detach().cpu()
                targets = batch[1].detach().cpu()

                # check if images are half or full
                if preds.shape[-2] != preds.shape[-1]:
                    preds = apply_symmetry(preds)
                    targets = apply_symmetry(targets)

                ifft_preds.extend(get_ifft(preds))
                ifft_targets.extend(get_ifft(targets))

            return (
                torch.stack(ifft_preds).detach().cpu().numpy(),
                torch.stack(ifft_targets).detach().cpu().numpy(),
            )

        case _:
            raise ValueError(
                f"No task {task!r} known. Available are 'inference' and 'training'."
            )


def get_ifft(image, amp_phase=False, scale=False, uncertainty=False) -> torch.Tensor:
    """Get inverse FFT of provided image data.

    Returns
    -------
    torch.tensor
        Inverse FFT of provided image data.
    """
    if isinstance(image, np.ndarray):
        image = torch.from_numpy(image)

    if len(image.shape) == 3:
        image = image.unsqueeze(0)

    compl = image[..., 0, :, :] + image[..., 1, :, :] * 1j

    if compl.shape[0] == 1:
        compl = compl.squeeze(0)

    return torch.abs(torch.fft.ifftshift(torch.fft.ifft2(torch.fft.fftshift(compl))))


def apply_symmetry(image) -> torch.Tensor:
    """Applies symmetry operations on an array.

    This follows Figure 5.3 in http://dx.doi.org/10.17877/DE290R-24834

    Parameters
    ----------
    image : array_like
        Input array of half images.
    uncertainty : bool, optional
        Whether image data contains uncertainty data.
        Default: False

    Returns
    -------
    symmetrical : torch.tensor
        Torch tensor containing the symmetrical image.
    """
    if isinstance(image, np.ndarray):
        image = torch.from_numpy(image)

    if image.ndim == 3:
        image = image.unsqueeze(0)

    *_, H, W = image.shape

    # Assume images are square; get target height from full width
    half_width = W // 2

    # Calculate the overlap from difference of half_image and
    # input height H, so we do not need to pass it anymore
    overlap = H - half_width

    pad_bottom = half_width - overlap
    full_image = F.pad(image, pad=(0, 0, 0, pad_bottom), mode="constant", value=0)

    upper_half = image[..., :half_width, :]

    # flip along image axes W and H to rotate image by 180 deg
    rotated = upper_half.flip(-2, -1)

    # Shift columns to the right by 1 to account for central pixel
    # and drop last row
    lower_half = torch.roll(rotated, shifts=1, dims=-1)
    lower_half = lower_half[..., :-1, :]
    lower_half[..., 1, :, :] *= -1

    full_image[..., half_width + 1 :, :] = lower_half

    return full_image
