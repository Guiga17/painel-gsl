
import streamlit as st
import requests
from PIL import Image

API_KEY = st.secrets["RIOT_API_KEY"]
REGION = "br1"
AMERICAS = "americas"

# Carrega o logo
logo = Image.open("logo_gsl.png")
st.image(logo, width=200)
st.title("📊 GSL – Estatísticas de Partidas Personalizadas")

summoner_name = st.text_input("Digite o nome do jogador:")

def get_summoner_data(name):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json()

def get_match_ids(puuid, count=50):
    url = f"https://{AMERICAS}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json()

def get_match_data(match_id):
    url = f"https://{AMERICAS}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    r = requests.get(url, headers={"X-Riot-Token": API_KEY})
    return r.json()

if summoner_name:
    summoner = get_summoner_data(summoner_name)
    if "puuid" in summoner:
        puuid = summoner["puuid"]
        matches = get_match_ids(puuid, count=50)
        st.subheader(f"Últimas partidas personalizadas de {summoner_name}")
        for match_id in matches:
            match = get_match_data(match_id)
            if match["info"]["gameMode"] == "CUSTOM":
                st.markdown(f"### Partida: {match_id}")
                for p in match["info"]["participants"]:
                    st.write(f"**{p['summonerName']}** – {p['championName']} – KDA: {p['kills']}/{p['deaths']}/{p['assists']}")
                st.markdown("---")
    else:
        st.error("Jogador não encontrado.")
