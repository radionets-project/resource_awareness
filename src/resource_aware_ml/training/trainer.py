"""Adapted from radionets source code

https://github.com/radionets-project/radionets

Under the MIT License
"""

from lightning import LightningModule


class TrainModule(LightningModule):
    def __init__(self, train_config: dict) -> None:
        super().__init__()
        self.save_hyperparameters()
        
        self.model = train_config["model"]()
        self.loss_fn = train_config["loss_fn"]()
        self.optimizer = train_config["optimizer"]
        self.lr = train_config["lr"]

    def forward(self, inputs):
        return self.model(inputs)

    def training_step(self, batch, batch_idx):
        inputs, targets = self._extract_inputs_targets(batch)

        preds = self(inputs)
        loss = self.loss_fn(preds, targets)
        self.log("train_loss", loss, prog_bar=True, sync_dist=True)

        return loss

    def validation_step(self, batch, batch_idx):
        inputs, targets = self._extract_inputs_targets(batch)

        preds = self(inputs)
        loss = self.loss_fn(preds, targets)
        self.log("val_loss", loss, prog_bar=True, sync_dist=True)

        return loss

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        inputs, _ = self._extract_inputs_targets(batch)
        preds = self(inputs)

        return preds

    def _extract_inputs_targets(self, batch):
        if isinstance(batch, dict):
            inputs = batch["inputs"]
            targets = batch.get("target", None)
        elif isinstance(batch, list | tuple):
            if len(batch) >= 2 and hasattr(batch[1], "__array__"):
                inputs, targets = batch[0], batch[1]
            else:
                inputs, targets = batch[0], None
        else:
            inputs, targets = batch, None

        return inputs, targets

    def configure_optimizers(self):
        optimizer = self.optimizer(self.parameters(), lr=self.lr)

        return {"optimizer": optimizer}
