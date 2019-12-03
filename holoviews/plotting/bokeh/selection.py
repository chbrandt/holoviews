from ...selection import OverlaySelectionDisplay
from ...core.options import Store


class BokehOverlaySelectionDisplay(OverlaySelectionDisplay):
    """
    Overlay selection display subclass for use with bokeh backend
    """
    def _build_element_layer(
            self, element, layer_color, selection_expr=True
    ):
        element, visible = self._select(element, selection_expr)

        backend_options = Store.options(backend='bokeh')
        style_options = backend_options[(type(element).name,)]['style']

        def alpha_opts(alpha):
            options = dict()

            for opt_name in style_options.allowed_keywords:
                if 'alpha' in opt_name:
                    options[opt_name] = alpha

            return options

        layer_alpha = 1.0 if visible else 0.0
        merged_opts = dict(self._get_color_kwarg(layer_color), **alpha_opts(layer_alpha))
        layer_element = element.options(tools=['box_select'], **merged_opts)

        return layer_element

    def _style_region_element(self, region_element, region_color):
        backend_options = Store.options(backend="bokeh")
        element_name = type(region_element).name
        style_options = backend_options[(element_name,)]['style']
        options = {}
        for opt_name in style_options.allowed_keywords:
            if 'alpha' in opt_name:
                options[opt_name] = 1.0
        options["color"] = region_color
        if element_name != "Histogram":
            options["line_width"] = 2
        return region_element.options(**options)
