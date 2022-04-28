#!~/bin/bash
for OPT in 2d_sparse 2d_dense 3d depth pncc pose uv_tex ply obj; do
  python3 demo.py -f ../3DDFA_V2/жуков_тест.jpg -o $OPT --show_flag=false --onnx;
done;
