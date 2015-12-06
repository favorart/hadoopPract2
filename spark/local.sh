#!/bin/sh

cat is5_all_lenta_2sides_graph/part-* | python numerate.py urls.txt new_urls.txt > numerated
cat numerated | python reshape.py graph_pr graph_hits