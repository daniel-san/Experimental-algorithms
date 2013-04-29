set grid
unset border
set style arrow 1 nohead lw 1

plot "cycle.data" using 1:2:($3-$1):($4-$2) with vectors arrowstyle 1 notitle, \
     "cycle.data" using 1:2 lt -1 pt 4 notitle, \
     "cycle.data" using 3:4 lt -1 pt 4 notitle

pause -1
