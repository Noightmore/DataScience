cd ./recordings
for f in *","*; do
  mv "$f" "${f//,/}"
done
