"""
Metron AI ArDaGen extension.
"""
import typing
import omni.ext
from omni import ui
import omni.kit.pipapi

omni.kit.pipapi.install("typeguard", module="typeguard")

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.


class ArDaGenExt(omni.ext.IExt):
    """
    Metron AI ArDaGen Extension.
    """

    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id: typing.Any) -> None:  # pylint: disable=unused-argument
        """
        On startup routine.

        Args:
            ext_id (Any): Extension id.
        """
        print("[metron.ai.ardagen] Metron AI ArDaGen Ext startup")

        self._window = ui.Window(  # pylint: disable=attribute-defined-outside-init
            "Metron AI ArDaGen Ext", width=300, height=300
        )
        with self._window.frame:
            with ui.VStack():
                ui.Label("Some Labels")

                def on_click() -> None:
                    print("clicked!")

                ui.Button("Me", clicked_fn=lambda: on_click())  # pylint: disable=unnecessary-lambda

    def on_shutdown(self) -> None:  # pylint: disable=no-self-use
        """
        On shutdown routine.
        """
        print("[metron.ai.ardagen] Metron AI ArDaGen Ext shutdown")
