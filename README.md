# Royale-API
Get your clash royale stats and save them to PDF.

### Installation:

```console
git clone https://github.com/antar/Royale-API
cd Royale-API
pip install requests && pip install fpdf
```
Create a bearer token on https://developer.clashroyale.com/#/register and set your IP (https://whatismyipaddress.com/de/meine-ip).
```console
cd Royale-API
echo "token" >> ./token.txt
```
### Examples:
```console
python data.py "#G9YV9GR8R"
python data.py "#QCCJVJR9"
```
The email parameter is optional and works correctly if you have set the smpt requirements.

### Output:
PDF will be created in the root folder ~/Royale-API/[data.pdf](https://github.com/antar/Royale-API/files/8451558/data.pdf)

## Author

* **antar** - *Initial work* - [antar](https://github.com/antar)
