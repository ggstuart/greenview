import greenview
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
fmt = DateFormatter('%d %b')

ws = greenview.WebService()

labels = {
    213: 'Queens',
    69: 'IOCT',
    111: 'Kimberlin Library',
    15: 'Campus Centre',
    490: 'Hugh Aston',
}

#meter_ids = [213, 69, 111, 15, 490]
fig = plt.figure()
fig.canvas.set_window_title("Greenview") 
plt.suptitle('Latest Week')
for meter_id in sorted(labels):# meter_ids:
#    meter = ws.Meter(meter_id)
    latestWeek = ws.GraemeLatestWeek(meter_id)
    data = latestWeek.data()
    plt.plot(data['datetime'], data['value'], label=labels[meter_id])#meter.description)
    plt.grid(True)
leg = plt.legend(loc='best')
leg.get_frame().set_alpha(0.15)
plt.axes().xaxis.set_major_formatter(fmt)
plt.show()
