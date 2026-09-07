"""Adapted from radionets source code

https://github.com/radionets-project/radionets

Under the MIT License
"""

from torch import nn

from .blocks import SRBlock

__all__ = [
    "SRResNet",
    "SRResNet4",
    "SRResNet6",
    "SRResNet10",
    "SRResNet18",
]


_PRE_BLOCK_KWARGS = dict(
    in_channels=2,
    out_channels=64,
    kernel_size=9,
    stride=1,
    padding=4,
    groups=2,
)

_FINAL_KWARGS = dict(
    in_channels=64,
    out_channels=2,
    kernel_size=9,
    stride=1,
    padding=4,
    groups=2,
)

_RES_BLOCK_KWARGS = dict(in_channels=64, out_channels=64)


class SRResNet(nn.Module):
    def __init__(
        self,
        pre_block_kwargs: dict | None = None,
        res_blocks_kwargs: dict | None = None,
        final_kwargs: dict | None = None,
    ):
        super().__init__()

        self.res_blocks_kwargs = res_blocks_kwargs
        if not self.res_blocks_kwargs:
            self.res_blocks_kwargs = _RES_BLOCK_KWARGS

        if not pre_block_kwargs:
            pre_block_kwargs = _PRE_BLOCK_KWARGS

        if not final_kwargs:
            final_kwargs = _FINAL_KWARGS

        self.preBlock = nn.Sequential(
            nn.Conv2d(**pre_block_kwargs),  # ty:ignore[invalid-argument-type]
            nn.PReLU(),
        )

        self.final = nn.Sequential(
            nn.Conv2d(**final_kwargs),  # ty:ignore[invalid-argument-type]
            nn.PReLU(),
        )

    def _create_blocks(self, n_blocks, **kwargs):
        blocks = []
        for _ in range(n_blocks):
            blocks.append(SRBlock(**self.res_blocks_kwargs, **kwargs))  # ty:ignore[invalid-argument-type]

        self.blocks = nn.Sequential(*blocks)

    def forward(self, input):
        x = self.preBlock(input)
        x = x + self.blocks(x)
        x = self.final(x)

        return x


class SRResNet18(SRResNet):
    def __init__(self):
        super().__init__()

        # Create 8 ResBlocks to build a SRResNet18
        self._create_blocks(8)


class SRResNet10(SRResNet):
    def __init__(self):
        super().__init__()

        # Create 4 ResBlocks to build a SRResNet10
        self._create_blocks(4)


class SRResNet6(SRResNet):
    def __init__(self):
        super().__init__()

        # Create 2 ResBlocks to build a SRResNet6
        self._create_blocks(2)


class SRResNet4(SRResNet):
    def __init__(self):
        super().__init__()

        # Create 1 ResBlocks to build a SRResNet4
        self._create_blocks(1)
