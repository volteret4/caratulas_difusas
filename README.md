# Carátulas Difusas

Juego web: aparece la portada de un disco muy difuminada y se va volviendo nítida poco a poco. Hay que acertar el disco entre 4 opciones; cuanto antes aciertes, más puntos.

## Añadir discos

1. Añade líneas `Artista | Álbum` a `tools/albums.txt`.
2. Ejecuta `python3 tools/build.py` (busca la portada en la API de iTunes y regenera `albums.json`; los discos ya resueltos no se vuelven a buscar).
3. Haz commit y push.

## Ajustes

En `index.html`: `ROUNDS` (rondas por partida), `DURATION` (ms hasta quedar nítida) y `MAX_BLUR` (desenfoque inicial).

## Probar en local

```bash
python3 -m http.server 8000
```
