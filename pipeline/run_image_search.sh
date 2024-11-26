
#!/bin/bash
python pipeline/D_image_search.py 1 5 &
python pipeline/D_image_search.py 2 5 &
python pipeline/D_image_search.py 3 5 &
python pipeline/D_image_search.py 4 5 &
python pipeline/D_image_search.py 5 5 &
wait