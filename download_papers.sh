#!/bin/bash

urls=(
    "https://openreview.net/pdf?id=VtmBAGCN7o"
    "https://openreview.net/pdf?id=6PmJoRfdaK"
    "https://openreview.net/pdf?id=LzPWWPAdY4"
    "https://openreview.net/pdf?id=VTF8yNQM66"
    "https://openreview.net/pdf?id=hSyW5go0v8"
    "https://openreview.net/pdf?id=9WD9KwssyT"
    "https://openreview.net/pdf?id=yV6fD7LYkF"
    "https://openreview.net/pdf?id=hnrB5YHoYu"
    "https://openreview.net/pdf?id=WbWtOYIzIK"
    "https://openreview.net/pdf?id=c5pwL0Soay"
    "https://openreview.net/pdf?id=TpD2aG1h0D"
)

papers=(
    "metagpt.pdf"
    "longlora.pdf"
    "loftq.pdf"
    "swebench.pdf"
    "selfrag.pdf"
    "zipformer.pdf"
    "values.pdf"
    "finetune_fair_diffusion.pdf"
    "knowledge_card.pdf"
    "metra.pdf"
    "vr_mcl.pdf"
)

mkdir -p papers

for i in "${!urls[@]}"; do
    wget "${urls[$i]}" -O "papers/${papers[$i]}"
done
