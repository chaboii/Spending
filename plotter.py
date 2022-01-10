import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#config
cvs = 'Week52.csv'
travels = ['','','','','Cabo','Beach','Turkey','Turkey','Egypt','Egypt','','Puerto Rico','Vegas/GC & Santa Barbara']

#plot setup
kw = dict(width_ratios=[1,2538/4408],height_ratios=[2,1])
fig,ax = plt.subplots(2,2, gridspec_kw=kw)
gs = ax[1,0].get_gridspec()
for a in ax[1,:]:
    a.remove()
axbig = fig.add_subplot(gs[1,:])

#monthly bar chart
axbig.title.set_text("\"Other\" Spending By Psuedo-Month")
df = pd.read_csv(cvs)
df['category']=df['category'].astype('category')
weeks4 = df['week4'].max()
cats = df.category.cat.categories
cat_totals = np.zeros(len(cats))
weeklytotal = 0
for i in range(1,weeks4+1):
    bot = 0
    week = df[df.week4==i]
    axbig.set_prop_cycle(None)
    for j,c in enumerate(cats):
        total = week[week.category==c].amount.sum()
        p = axbig.bar(i,total,bottom=bot)
        bot+=total
        cat_totals[j]+=total
    weeklytotal+=bot
    axbig.annotate('{}'.format(travels[i-1]), xy=(i,bot),xytext=(0, 0), rotation = 30, textcoords="offset points",ha='center', va='bottom')    
monthlyavg = weeklytotal/weeks4/4*4.34

#labels for monthly bar chart
axbig.legend(cats)
axbig.set_xlabel("Week/4")
axbig.set_ylabel("$")

#monthly pie chart
labels = 'rent','utilties','car','other'
sizes = [1500,230,140,monthlyavg]
total = sum(sizes)
explode = (0,0,0,0.1)
ax[0,0].pie(sizes,explode=explode,labels=labels,shadow=True,startangle=90, autopct=lambda p: '{:.0f}'.format(p * total / 100))
ax[0,0].title.set_text("Monthly Spending: "+r"$\bf{\$ %s}$" % str(round(total)))

#other monthly pie chart
explodes = [0.05 for i in cats]
ax[0,1].pie(cat_totals,labels=cats,shadow=True,startangle=90, autopct=lambda p: '{:.0f}'.format(p * monthlyavg / 100))
ax[0,1].title.set_text("\"Other\" Category Per Month: "+r"$\bf{\$ %s}$" % str(round(monthlyavg)))

plt.show()