

class DrawParadox:

	def draw(canvas, points, center=[], turn='left', layers=1, starting_index=0):
		alpha = .2
		angles = len(points)

		canvas.create_line(points[0], points[1])
		canvas.create_line(points[1], points[2])
		canvas.create_line(points[2], points[0])

		canvas.create_rectangle(center[0]-1, center[1]-1, center[0]+1, center[1]+1)	

		for layer in range(layers):

			for idx in range(len(points)):

				first_point = points[idx]
				second_point = points[(idx+1)%angles]
				third_point = points[(idx+2)%angles]

				target_x = first_point[0] + alpha*(abs(second_point[0] - third_point[0]))
				target_y = first_point[1] + alpha*(abs(second_point[1] - third_point[1]))

				points[(idx+1)%angles] = (target_x, target_y)

				canvas.create_line(first_point, points[(idx+1)%angles], width=5)
				print(first_point, points[(idx+1)%angles])