from tkinter import Tk, Canvas
from functools import partial

def get_common_point(a1, a2, a3, a4):
	x1, y1, x2, y2, x3, y3, x4, y4 = *a1, *a2, *a3, *a4
	try:
		x = 	((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
		y = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
		return [x, y]
	except:
		return False

def inside_polygon(x, y, points):
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def draw(canvas, points, center, turn, layers, event=False):
	if event:
		center = (event.x, event.y)

	points = points[:]
	alpha = .1
	angles = len(points)

	if turn == 'left':
		points = points[::-1]
	
	for angle in range(angles):
		canvas.create_line(points[angle], points[(angle+1)%angles], width=2)

	for layer in range(layers):

		for idx in range(len(points)):
			first_point = points[idx]
			second_point = points[(idx+1)%angles]
			third_point = points[(idx+2)%angles]

			common_point = get_common_point(first_point, center, second_point, third_point)
			if not common_point or (second_point[0] - common_point[0])**2 + (second_point[1] - common_point[1])**2 > (second_point[0] - third_point[0])**2 + (second_point[1] - third_point[1])**2:
				common_point = third_point

			target_x = second_point[0] + alpha*(common_point[0] - second_point[0])
			target_y = second_point[1] + alpha*(common_point[1] - second_point[1])

			points[(idx+1)%angles] = (target_x, target_y)

			canvas.create_line(first_point, points[(idx+1)%angles], width=1)


class CanvasManager:

	def __init__(self, canvas):
		self.figures = []
		self.canvas = canvas

	def add_figure(self, points, center, turn='roght', layers=40):
		self.figures.append({
			'points': points,
			'center': center,
			'turn': turn,
			'layers': layers
			})

	def modify_center(self, event):
		for idx, figure in enumerate(self.figures):
			if inside_polygon(event.x, event.y, figure['points']):
				self.figures[idx]['center'] = (event.x, event.y)
				self.compose()
				break

	def compose(self):
		self.canvas.delete('all')

		for figure in self.figures:
			draw(self.canvas, figure['points'], figure['center'], figure['turn'], figure['layers'])

	def clear(self):
		self.figures = []
		self.canvas.delete('all')		

def main():
	managers = []
	canvases = []
	for h in range(3):
		for w in range(3):
			canvases.append(Canvas(root, width=600, height=300))
			managers.append(CanvasManager(canvases[-1]))

			managers[-1].add_figure([(0,0), (600,0), (300,150)], (300, 70))
			managers[-1].add_figure([(0,0), (0,300), (300,150)], (150, 150), 'left')
			managers[-1].add_figure([(600,0), (600,300), (300,150)], (450, 150), 'left')
			managers[-1].add_figure([(0,300), (600,300), (300,150)], (300, 250))
			
			managers[-1].compose()

			canvases[-1].bind('<B1-Motion>', managers[-1].modify_center)
			canvases[-1].bind('<Button-1>', managers[-1].modify_center)

			canvases[-1].grid(column=w, row=h)

if __name__ == '__main__':
	root = Tk()
	main()
	root.mainloop()