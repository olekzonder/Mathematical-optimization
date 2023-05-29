from point import Point


def dominates(p,q):
     return p.f1 >= q.f1 and p.f2 >= q.f2 and (p.f1 > q.f1 or p.f2 > q.f2)

def filter_optimal(points):
    n = len(points)
    dominated = set()
    for i in range(n):
        if i in dominated:
            continue
        for j in range(i+1, n):
            if dominates(points[i], points[j]):
                dominated.add(j)
            elif dominates(points[j], points[i]):
                dominated.add(i)
                break
    return [points[i] for i in range(n) if i in dominated],[points[i] for i in range(n) if i not in dominated]


class Linear:
    def __init__(self,w1,w2):
        self.w1 = w1
        self.w2 = w2
    
    def linear_combination(self,p):
        return self.w1 * p.f1 + self.w2 * p.f2

    def linear_optimal(self,unopt,pareto):
        optimal = [max(pareto, key=self.linear_combination)]
        return [unopt,pareto,optimal]
    
class Hermeyer:
    def __init__(self):
        pass
    def hermeyer(self,p):
        return min([p.f1,p.f2])

    def hermeyer_optimal(self,unopt,pareto):
        optimal = [max(pareto, key=self.hermeyer)]
        return [unopt,pareto,optimal]



def ideal_point(points,unopt,pareto):
    max_f1 = max(point.f1 for point in points)
    max_f2 = max(point.f2 for point in points)
    ideal = Point(max_f1, max_f2)

    for point in pareto:
        point.distance = point.distance_to(ideal)

    optimal = [min(pareto, key = lambda point: point.distance)]
    return [unopt,pareto,optimal,[ideal]]


class Threshold:
    def __init__(self,criterion,threshold):
        self.criterion = criterion
        self.threshold = threshold

    def threshold_optimal(self,unopt,pareto):
        if self.criterion == 'f1':
            optimal = [point for point in pareto if point.f2 > self.threshold]
            try:
                most_optimal = [max(optimal,key = lambda point: point.f1)]
            except:
                most_optimal = []
        else:
            optimal = [point for point in pareto if point.f1 > self.threshold]
            try:
                most_optimal = [max(optimal,key = lambda point: point.f2)]
            except:
                most_optimal = []
        return [unopt,pareto,optimal,most_optimal]