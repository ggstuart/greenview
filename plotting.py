import greenview
from matplotlib import pyplot as plt
ws = greenview.WebService()
meter_ids = [213, 69, 111, 15, 490]

plt.figure()
for meter_id in meter_ids:
    latestWeek = ws.GraemeLatestWeek(meter_id)
    data = latestWeek.data()
    plt.plot(data['datetime'], data['value'])
plt.show()
