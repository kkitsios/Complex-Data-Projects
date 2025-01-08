# Konstantinos Kitsios, A.M. 4388, cse84388
import csv

GRID_DIR_FILE = 'grid.dir'
GRID_GRD_FILE = 'grid.grd'
DATASET = 'tiger_roads.csv'
GRID_SIZE = 10

def overlaps(rect1, rect2):

    return not (rect1[2] < rect2[0] or  # rect1 is left of rect2
                rect1[0] > rect2[2] or  # rect1 is right of rect2
                rect1[3] < rect2[1] or  # rect1 is above rect2
                rect1[1] > rect2[3])    # rect1 is below rect2


def find_mbr(coords):
    min_lon = float('inf')
    min_lat = float('inf')
    max_lon = float('-inf')
    max_lat = float('-inf')
    for coord in coords:
        lon, lat = map(float, coord.split())
        if lon < min_lon:
            min_lon = lon
        if lat < min_lat:
            min_lat = lat
        if lon > max_lon:
            max_lon = lon
        if lat > max_lat:
            max_lat = lat
    return [min_lon, min_lat, max_lon, max_lat]

def read_data(filename):
    records = {}
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    with open(filename, 'r') as dataset:
        num_lines = int(dataset.readline().strip())
        for i in range(num_lines):
            row = dataset.readline().strip().split(',')
            coords = [list(map(float, c.split(' '))) for c in row]
            mbr = find_mbr(row)
            records[i+1]= (mbr, coords)
            for coord in coords:
                 min_x = min(min_x, coord[0])
                 max_x = max(max_x, coord[0])
                 min_y = min(min_y, coord[1])
                 max_y = max(max_y, coord[1])
    return records,min_x,max_x,min_y,max_y

def create_cells(records, min_x, max_x, min_y, max_y):

    range_x = max_x - min_x
    range_y = max_y - min_y
    grid_size_x = range_x / GRID_SIZE
    grid_size_y = range_y / GRID_SIZE
    cells = {}

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_coords = (i, j)
            cells[cell_coords] = []

    for record in records:
        id = record
        mbr = records[id][0]
        coords =records[id][1]
        cell_coords = []

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cellc = (i,j)
                cell_min_x = min_x + i * grid_size_x
                cell_max_x = min_x + (i+1) * grid_size_x
                cell_min_y = min_y + j * grid_size_y
                cell_max_y = min_y + (j+1) * grid_size_y
                if overlaps(mbr, [cell_min_x, cell_min_y, cell_max_x, cell_max_y]):
                    cell_coords.append((i, j))

        for c in cell_coords:
            if c not in cells:
                cells[c] = []
            cells[c].append(id)
            
    return cells, grid_size_x, grid_size_y

def write_dir_file(min_x, max_x, min_y, max_y, cells):
    with open(GRID_DIR_FILE, 'w') as f:
        f.write("%f %f %f %f\n"  %(min_x, min_y, max_x, max_y))
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell_coords = (i, j)
                cell_contents = sorted(cells.get(cell_coords, []))
                f.write("%d %d %d\n" %(i, j, len(cell_contents)))



def write_grd_file(min_x, max_x, min_y, max_y, cells, grid_size_x, grid_size_y, records):
    with open(GRID_GRD_FILE, 'w') as f_out:
        cells_sorted = sorted(cells.items())
        for cell_coords, cell_contents in cells_sorted:
            i, j = cell_coords
            cell_contents = sorted(cell_contents)
            cell_mbr = None  # initialize cell mbr
            for obj_id in cell_contents:
                obj_mbr = records[obj_id ][0]
                obj_coords = records[obj_id ][1]
                coords_str = ', '.join([f"{c[0]} {c[1]}" for c in obj_coords])
                coords_str = coords_str[:-2] # remove last comma and space
                f_out.write(f"{obj_id}, {obj_mbr[0]} {obj_mbr[1]}, {obj_mbr[2]} {obj_mbr[3]}, ")
                f_out.write(f"{coords_str}\n") # don't add comma here




def main():
    records,min_x,max_x,min_y,max_y = read_data(DATASET)
    cells, grid_size_x, grid_size_y = create_cells(records, min_x, max_x, min_y, max_y)
    write_dir_file(min_x, max_x, min_y, max_y, cells)
    write_grd_file(min_x, max_x, min_y, max_y, cells, grid_size_x, grid_size_y, records)
main()