# Them cac thu vien neu can
import math
import random

def calc_distance(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def pay_per_order(v,m):
    return 5 + int(v) + 2*int(m)

class Shipper:
    def __init__(self,base,firstOrder):
        self.h = firstOrder.pay - (calc_distance(base,firstOrder.coord)*0.5+10)
        self.traverse = [firstOrder]
        self.last = firstOrder

    def addOrder(self,order):
        self.h += order.pay - calc_distance(self.last.coord,order.coord)*0.5
        self.traverse.append(order)
        self.last = order

    def printList(self):
        first = True
        for ele in self.traverse:
            if first:
                print(str(ele.index),end='')
                first = False
            else:
                print(' ' + str(ele.index),end='')
        print()

class Order:
    def __init__(self,i,p,t):
        self.index = i
        self.pay = p
        self.coord = t

def heuristic(lst,nextOrder):
    temp = []
    temp2 = []
    for shipper in lst:
        nextVal = nextOrder.pay - calc_distance(shipper.last.coord,nextOrder.coord)*0.5
        sum = 0
        sum2 = 0
        for anotherShipper in lst:
            if shipper == anotherShipper:
                pass
            sum += abs(shipper.h - anotherShipper.h + nextVal)
            sum2 += abs(shipper.h - anotherShipper.h)
        temp.append(sum)
        temp2.append(sum2)
    
    h_of_each_shipper = []
    for i in range(len(lst)):
        total_h = temp[i]+math.fsum(temp2)-temp2[i]
        h_of_each_shipper.append(total_h)

    # Append shipper that has min heuristic value
    minIdx = min(range(len(h_of_each_shipper)), key=h_of_each_shipper.__getitem__)
    lst[minIdx].addOrder(nextOrder)

def heuristic_total(lst):
    total = 0
    for shipper in lst:
        sum = 0
        for anotherShipper in lst:
            if shipper == anotherShipper:
                pass
            #TODO
            sum += abs(shipper.h - anotherShipper.h)
        #print(sum)
        total+= sum
    return total

def random_order(shipper_count,orders,shippers,base_coord):
    for i in range(0,shipper_count):
        r = random.choice(orders)
        shippers.append(Shipper(base_coord,r))
        orders.remove(r)

    count = len(orders)
    while count > 0:
        r = random.choice(orders)
        heuristic(shippers,r)
        orders.remove(r)
        count-=1
    return (shippers,heuristic_total(shippers))

def assign(file_input, file_output):

    orders = []
    shippers = []
    # read input
    input = open(file_input)
    count_line = 0
    for line in input:
        data = line.split(' ')
        if count_line == 0:
            # data[1] chứa kí tự /n ở cuối: 5/n -> dùng [:-1] để cắt
            base_coord = (int(data[0]),int(data[1][:-1]))
        elif count_line == 1:
            order_count = int(data[0])
            shipper_count = int(data[1][:-1])
        else:
            # save order infomation: index (start from 0), coordinate - data[0] and data[1],
            # volume - data[2], mass - data[3]

            # Each order has 3 attribute: index, coord, pay
            coord = (int(data[0]),int(data[1]))
            if len(orders)+1 == order_count:
                #temp_order = (len(orders),coord,pay_per_order(data[2],data[3]))
                temp = Order(len(orders),pay_per_order(data[2],data[3]),coord)
            else:
                #temp_order = (len(orders),coord,pay_per_order(data[2],data[3][:-1]))
                temp = Order(len(orders),pay_per_order(data[2],data[3][:-1]),coord)

            orders.append(temp)
        count_line+=1
    input.close()

    # Run Algorithm

    # Assign random m orders for m shipper from n-orders (m < n)
    randomList = []
    minVal = (None,99999999)

    randomRange = 1
    if order_count < 100:
        randomRange = 200
    elif order_count >= 100 and order_count < 200:
        randomRange = 10

    for i in range(0,randomRange):
        randomList.append(random_order(shipper_count,orders[:],shippers[:],base_coord))

    for item in randomList:
        #print(item[1])
        if item[1] < minVal[1]:
            minVal = item

    shippers = minVal[0]
    #print(minVal[1])

    # write output

    output = open(file_output, 'w')
    firstRoute = True
    for sp in shippers:
        listToStr = ' '.join([str(ele.index) for ele in sp.traverse])
        if firstRoute:
            output.write(listToStr)
            firstRoute = False
        else:
            output.write('\n'+listToStr)
    output.close()

    return

// Run 25 testcase
for i in range(25):
    index = i + 1
    assign('input/' + index + '.txt', 'output/' + index + '.txt')
