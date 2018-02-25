from tkinter import Tk, Canvas
from drawer import DrawParadox

def get_common_point(a1, a2, a3, a4):
	x1, y1, x2, y2, x3, y3, x4, y4 = *a1, *a2, *a3, *a4
	x = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
	y = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

	return [x, y]

def pre_draw(event):
	canvas.delete("all")
	draw(canvas, [(0,10), (1499,10), (1500,1000)], (event.x, event.y))

def draw(canvas, points, center, turn='right', layers=100, starting_index=0):
	alpha = .1
	angles = len(points)

	if turn == 'left':
		points = points[::-1]
	
	for angle in range(angles):
		canvas.create_line(points[angle], points[(angle+1)%angles], width=2)

	canvas.create_rectangle(center[0]-1, center[1]-1, center[0]+1, center[1]+1)

	for layer in range(layers):

		for idx in range(len(points)):
			first_point = points[idx]
			second_point = points[(idx+1)%angles]
			third_point = points[(idx+2)%angles]

			common_point = get_common_point(first_point, center, second_point, third_point)

			target_x = second_point[0] + alpha*(common_point[0] - second_point[0])
			target_y = second_point[1] + alpha*(common_point[1] - second_point[1])

			points[(idx+1)%angles] = (target_x, target_y)

			canvas.create_line(first_point, points[(idx+1)%angles], width=1)

def main():
	draw(canvas, [(0,10), (1499,10), (1500,1000)], (1000, 500))
	canvas.bind('<B1-Motion>', pre_draw)
	canvas.bind('<Button-1>', pre_draw)

if __name__ == '__main__':
	root = Tk()
	canvas = Canvas(root, width=1920, height=1080)
	main()
	canvas.grid()
	root.mainloop()