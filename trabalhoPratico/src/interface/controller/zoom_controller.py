class ZoomController:

    def setup_zoom_and_drag(self, canvas, ax):
        def on_press(event):
            if event.button == 1:
                canvas.mpl_connect('motion_notify_event', on_drag)
                canvas.mpl_connect('button_release_event', on_release)
                on_press.x0, on_press.y0 = event.xdata, event.ydata

        def on_release(event):
            canvas.mpl_disconnect(canvas.mpl_connect('motion_notify_event', on_drag))
            canvas.mpl_disconnect(canvas.mpl_connect('button_release_event', on_release))

        def on_drag(event):
            if event.inaxes and event.button == 1:
                dx = event.xdata - on_press.x0
                dy = event.ydata - on_press.y0
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
                ax.set_ylim(ylim[0] - dy, ylim[1] - dy)
                canvas.draw()

        def on_zoom(event):
            if event.inaxes:
                scale_factor = 0.9 if event.button == 'up' else 1.1
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                xdata = event.xdata
                ydata = event.ydata

                new_xlim = [xdata + (x - xdata) * scale_factor for x in xlim]
                new_ylim = [ydata + (y - ydata) * scale_factor for y in ylim]

                ax.set_xlim(new_xlim)
                ax.set_ylim(new_ylim)
                canvas.draw()

        canvas.mpl_connect('button_press_event', on_press)
        canvas.mpl_connect('scroll_event', on_zoom)
