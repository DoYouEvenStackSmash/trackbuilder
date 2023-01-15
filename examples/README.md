# Example
To verify behavior: \\

```python3 ../src/trackbuilder.py reload template.json ./ final.json``` <br>
This will output a valid but empty file titled `final.json` to stdout.  <br>

For failsafe reasons, overwriting a file of the same name with reload is not permitted. (For those who would prefer streamlined workflow, this behavior can be patched in `trackbuilder.py` in the ``reload`` function.)

