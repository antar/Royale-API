# Royale-API
Get your clash royale stats and save them to pdf.

### Installation

```console
git clone https://github.com/antar/Royale-API
cd Royale-API
pip install requests && pip install fpdf
```
Create a bearer token on https://developer.clashroyale.com/#/register and set your ip (https://whatismyipaddress.com/de/meine-ip).

Copy your token to the ~/Royale-API/token.txt file.

### Start: 
```console
python data.py "Your Clash Royale Tag" "Your Email Address"
```
The email parameter is optional and works correctly if you have set the smpt requirements.

### Examples:
```console
python data.py "#G9YV9GR8R"
python data.py "#QCCJVJR9"
```

### Output:
PDF will be created in the root folder ~/Royale-API/data.pdf

## Author

* **antar** - *Initial work* - [antar](https://github.com/antar)
