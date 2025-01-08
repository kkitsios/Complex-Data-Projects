# Konstantinos Kitsios, A.M. 4388, cse84388
GRID_DIR_FILE = 'grid.dir'
GRID_GRD_FILE = 'grid.grd'
GRID_SIZE = 10
QUERIES_FILE = 'queries.txt'


def rect_intersection(rect1, rect2):


    rect2 = [rect2[0],rect2[2], rect2[1], rect2[3]]
    if rect1[0] <= rect2[2] and rect1[2] >= rect2[0] and rect1[1] <= rect2[3] and rect1[3] >= rect2[1]:
        return True
    else:
        return False


def reconstruct_grid():
    cells = {}
    records = {}

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_coords = (i,j)
            cells[cell_coords] = []

    with open(GRID_DIR_FILE, 'r') as dir_file, open(GRID_GRD_FILE, 'r') as grd_file:
        # read the bounds of the dataset from the dir file
        bounds = dir_file.readline().strip().split()
        min_x, min_y, max_x, max_y = map(float, bounds)

        # read the cells from the dir file
        for line in dir_file:
            i, j, num_objects = map(int, line.strip().split())
            cell_coords = (i, j)
            cell_contents = [] 
            # read the object IDs from the grd file
            for _ in range(num_objects):
                line = grd_file.readline().strip()
                parts = line.strip().split(',')
                obj_id = int(parts[0])
                mbr = [float(parts[1].split()[0]), float(parts[1].split()[1]), float(parts[2].split()[0]), float(parts[2].split()[1])]
                coords = [float(coord) for coord in ' '.join(parts[3:]).split()]
                cell_contents.append(obj_id)

                # create a new record for the object and add it to the records dictionary
                if obj_id not in records:
                    records[obj_id] = {'mbr': mbr, 'coords':coords}

                cells[cell_coords] = cell_contents

    return cells, min_x, max_x, min_y, max_y, records

def process_queries():
    cells,min_x, max_x, min_y, max_y, records = reconstruct_grid()

    with open(QUERIES_FILE, 'r') as f:
        for line in f:
            query_id, window_coords = line.strip().split(',')
            query_id = int(query_id)
            window_coords = list(map(float, window_coords.split()))
            x1, x2, y1, y2 = window_coords
 
            # determine the cells that intersect with the query window
            cells_to_check = []
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    cell_coords = (i, j)
                    cell_bounds = [min_x+i*(max_x-min_x)/GRID_SIZE, min_y+j*(max_y-min_y)/GRID_SIZE,
                                   min_x+(i+1)*(max_x-min_x)/GRID_SIZE, min_y+(j+1)*(max_y-min_y)/GRID_SIZE]
                    if cell_bounds[2] >= x1 and cell_bounds[0] <= x2 and cell_bounds[3] >= y1 and cell_bounds[1] <= y2:
                        cells_to_check.append(cell_coords)

            # process each object in the cells that intersect with the query window
            results = []
            for cell_coords in cells_to_check:
                for obj_id in cells[cell_coords]:
                    mbr = records[obj_id]['mbr']
                    if mbr[2] >= x1 and mbr[0] <= x2 and mbr[3] >= y1 and mbr[1] <= y2:
                            ref_x = max(mbr[0], x1)
                            ref_y = max(mbr[1], y1)
                            if (ref_x >= min_x+cell_coords[0]*(max_x-min_x)/GRID_SIZE and 
                                ref_x < min_x+(cell_coords[0]+1)*(max_x-min_x)/GRID_SIZE and 
                                ref_y >= min_y+cell_coords[1]*(max_y-min_y)/GRID_SIZE and 
                                ref_y < min_y+(cell_coords[1]+1)*(max_y-min_y)/GRID_SIZE):
                        
                                results.append(obj_id)

            print("Query %d" %(query_id))
            print(sorted(results))
            print("Cells: %d" %(len(cells_to_check)))
            print("Results: %d" %(len(results)))
            print("----------")

process_queries()