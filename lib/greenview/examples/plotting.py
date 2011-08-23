import greenview
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
fmt = DateFormatter('%d %b')

class LatestWeekPlot(object):
    def __init__(self, labels = {213: 'Queens', 69: 'IOCT', 111: 'Kimberlin Library', 15: 'Campus Centre', 490: 'Hugh Aston'}):
        self.ws = greenview.WebService()
        self.labels = labels

    def show(self):
        fig = plt.figure()
        fig.canvas.set_window_title("Greenview") 
        plt.suptitle('Latest Week')
        for meter_id in sorted(self.labels):# meter_ids:
        #    meter = ws.Meter(meter_id)
            latestWeek = self.ws.GraemeLatestWeek(meter_id)
            data = latestWeek.data()
            plt.plot(data['datetime'], data['value'], label=self.labels[meter_id])#meter.description)
            plt.grid(True)
        leg = plt.legend(loc='best')
        leg.get_frame().set_alpha(0.15)
        plt.axes().xaxis.set_major_formatter(fmt)
        plt.show()
        
if __name__ == "__main__":
    lwp = LatestWeekPlot()
    lwp.show()
