## A python wrapper to learn muisc thoery

[**Read docs here**](http://guitar-harmony.readthedocs.io/en/latest/)

### Examples:
```python
$ python -i wapper.py
>>> generate_interval('Db', 'A5')
>>> ['A']
>>> generate_chord('E', '7')
>>> ['E', 'G#', 'B', 'D']
>>> generate_scale('F#', 'mixolydian')
>>> ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#']
>>> generate_progression('Ab', 'major_sevenths')
>>> ['Abmaj7', 'Bbm7', 'Cm7', 'Dbmaj7', 'Eb7', 'Fm7', 'Gm7b5', 'Abmaj7']
```

### To do:
> Transform note to pitch and/or frequency
>
> Generate random rhythm with a specific style
>
> Chordify melodic
>
> Generate according exercises
>
> Show('midi') and Show('scores')
>
> Integrate with `Aria Maestosa`
>
> Learn music by music (Neural networks)
>
> Music Visualization
>

### Based on the following books:
> [Harmony and Theory: A Comprehensive Source for All Musicians](https://www.amazon.com/Harmony-Theory-Comprehensive-Musicians-Essential/dp/0793579910)
>
> [Jazz Improvisation For Guitar - A Harmonic Approach](https://www.amazon.com/dp/0876391048/ref=pd_lpo_sbs_dp_ss_1?pf_rd_p=1944687662&pf_rd_s=lpo-top-stripe-1&pf_rd_t=201&pf_rd_i=0634017721&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=8ZX63RCG5PY74773KXAX)
>
> [The Advancing Guitarist](https://www.amazon.com/Advancing-Guitarist-Mick-Goodrick/dp/0881885894)
>
> [Ear Training for the Contemporary Musician](https://www.amazon.com/Ear-Training-Contemporary-Musician-Elliott/dp/0793581931/ref=sr_1_1?s=books&ie=UTF8&qid=1472993043&sr=1-1&keywords=ear+training+for+the+contemporary+musician)

### License:
This was made by Xi He [heeryerate@gmail.com](mailto:heeryerate@gmail.com).

### Reference:
> [GitHub/musthe](https://github.com/gciruelos/musthe)
>
> [GitHub/midiutil](https://github.com/duggan/midiutil)
>
> [music21](http://web.mit.edu/music21/)
>
> [Aria Maestosa](http://ariamaestosa.sourceforge.net/index.html)
>
> [Other resources](https://wiki.python.org/moin/PythonInMusic)

