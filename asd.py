from wikidata.client import Client
import wikipedia

client = Client()
entity = client.get('Q1617977', load=True)

url = entity.data['sitelinks']['frwiki']['url']

print(url)