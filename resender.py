#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tqdm
import codecs
import argparse
import requests
from requests.auth import HTTPProxyAuth
from bs4 import BeautifulSoup

url="https://club.pokemon.com/us/pokemon-trainer-club/activated"
#proxies = {'http': 'http://username:password@ip:port', 'https': 'http://username:password@ip:port'}
proxies = {}

def parseArgs():
    parser = argparse.ArgumentParser(description="Resend PTC accounts activation e-mail")
    parser.add_argument("-a", "--accts_file", help="KinanCity Core account file, that is, a csv with username;password;email")
    parser.add_argument("-l", "--links_file", help="KinanCity Mail links file, that is, a csv with type;link;email;status")
    parser.add_argument("-s", "--separator", default=";", help="File separator, defaults to ;")
    parser.add_argument("-pn", "--proxy_name", help="The URL to the proxy like 'http://username:password@ip:port'")

    args = parser.parse_args()

    return args


def parseFile(args):
    accts_data = []
    links_data = []

    with codecs.open(args.accts_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.strip()
            if len(line) < 1 or line[0] == "#":
                continue

            parts = line.split(args.separator)
            username = parts[0]
            password = parts[1]
            email = parts[2]

            accts_data.append({"username": username, "password": password, "email": email})

    with codecs.open(args.links_file, 'r', 'utf-8') as f:
        for line in f:
            line = line.strip()
            if len(line) < 1 or line[0] == "#":
                continue

            parts = line.split(args.separator)
            type = parts[0]
            link = parts[1]
            email = parts[2]
            status = parts[3]

            #links_data.append({"type": type, "link": link, "email": email, "status": status})
            links_data.append(email)

    print("Lines in account data: "+str(len(accts_data)))
    print("Lines in links data: "+str(len(links_data)))
    print("The follow emails were not found in links: #username;password;email")
    ret_accts_data = accts_data.copy() #Make a copy so we don't lose our index place by popping
    for index, acct_entry in enumerate(accts_data):
        #print(index, " Checking email: "+acct_entry['email'])
        try:
            idx = links_data.index(acct_entry['email'])
            #print("Index "+str(idx)+" found for: "+acct_entry['email'])
            if idx >= 0:
                ret_accts_data.remove(acct_entry)
        except Exception as e:
            #print(e)
            print(acct_entry['username']+";"+acct_entry['password']+";"+acct_entry['email'])
        
    print("Lines in return data: "+str(len(ret_accts_data)))
    return ret_accts_data


def getTokenAndCookies():
    resendPage = requests.get(url, proxies=proxies)

    if "Response [403]" in str(resendPage) or "ERROR 403" in str(resendPage):
        token=""
        resendPage.cookies=""
    else:
        soup = BeautifulSoup(resendPage.text, 'html.parser')
        csrfMiddlewareTokenInput = soup.find(attrs={"name": "csrfmiddlewaretoken"})
        token = csrfMiddlewareTokenInput.attrs['value']

    return token, resendPage.cookies


def resendActivation(email, password, username):
    token, cookies = getTokenAndCookies()

    if token == "":
        print("Error 403 when trying email: ", email)
    else:
        postData = {
            "csrfmiddlewaretoken": token,
            "email": email,
            "username": username,
            "password": password
        }

        postHeaders = {
            "authority": "club.pokemon.com",
            "referer": url
        }

        requests.post(url, data=postData, headers=postHeaders, cookies=cookies, proxies=proxies)


def main():
    args = parseArgs()
    accountsData = parseFile(args)

    if args.proxy_name:
        global proxies
        proxies={'http': args.proxy_name, 'https': args.proxy_name}

    for accountData in tqdm.tqdm(accountsData):
        resendActivation(accountData['email'], accountData['password'], accountData['username'])


if __name__ == '__main__':
    main()
