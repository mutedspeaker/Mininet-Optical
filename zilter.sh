while read -r input; do
  if [[ "$input" =~ ^(t[0-9]+) receiving \<ch([0-9]+):([0-9]+\.[0-9]+)THz\> at port [0-9]+: Success! gOSNR: ([0-9]+\.[0-9]+) dB OSNR: ([0-9]+\.[0-9]+) dB$ ]]; then
    t="${BASH_REMATCH[1]}"
    ch="${BASH_REMATCH[2]}"
    freq="${BASH_REMATCH[3]}"
    gosnr="${BASH_REMATCH[4]}"
    osnr="${BASH_REMATCH[5]}"
    echo "t=$t, ch=$ch, freq=$freq, gOSNR=$gosnr, OSNR=$osnr"
  fi
done < output.txt
