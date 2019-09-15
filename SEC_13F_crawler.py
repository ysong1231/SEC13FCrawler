import re
import xml.etree.ElementTree as ET
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import collections
import csv
import logging
from pandas import DataFrame

def generate_url(CIK, file_type = '13F-HR', date_before=''):
    return "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + CIK + "&type="+ file_type +"&dateb=" + date_before + "&owner=exclude&action=getcompany"

def get_xml(url, headless = True):
    options = webdriver.ChromeOptions()
    options.set_headless(headless)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    document_button = browser.find_element_by_id("documentsbutton")
    document_button.click()
    Wait(browser, 100).until(
        expected_conditions.presence_of_element_located(
            (By.XPATH, "//*[@id='formDiv']/div/table")
        )
    )
    date = browser.find_element_by_xpath("//*[@id='formDiv']/div[2]/div[1]/div[2]").text
    return browser.find_element_by_xpath("//*[@id='formDiv']/div/table/tbody/tr[5]/td[3]/a").get_attribute('href'), date

def parse_xml(xml_url):
    xml_str = urllib.request.urlopen(xml_url).read()
    xmldoc = ET.fromstring(xml_str)
    xml_table = []
    for child in xmldoc:
        row = {}
        for item in child:
            if 'votingAuthority' in item.tag:
                for col in item:
                    row['votingAuthority_' + re.sub('{.*}', '', col.tag)] = col.text
            elif 'shrsOrPrnAmt' in item.tag:
                for col in item:
                    row['shrsOrPrnAmt_' + re.sub('{.*}', '', col.tag)] = col.text
            else:
                row[re.sub('{.*}', '', item.tag)] = item.text
        xml_table.append(row)
    return xml_table

def write_to_file(table, name, date, path = './'):
    
    df = DataFrame(columns = ['nameOfIssuer', 
                              'titleOfClass', 
                              'cusip', 
                              'value', 
                              'shrsOrPrnAmt_sshPrnamt', 
                              'shrsOrPrnAmt_sshPrnamtType', 
                              'putCall', 
                              'investmentDiscretion', 
                              'otherManager', 
                              'votingAuthority_Sole', 
                              'votingAuthority_Shared', 
                              'votingAuthority_None']
                  )
    for row in table:
        new_row = DataFrame(row, index = [0])
        df = df.append(new_row, ignore_index=True, sort=False)
    df.to_csv(path + name + "_" + date + '.tsv',index = False, sep='\t', quoting=csv.QUOTE_NONE)

def main():
    query_CIK = input("Enter CIK: ")
    date_before = input("Date Prior to(YYYY-MM-DD): ")
    download_path = input("Enter download path:")
    
    logging.basicConfig(level=logging.INFO)
    logging.info("Process Start...")
    
    logging.info("Generating URL based on input...")
    url = generate_url(query_CIK, date_before = date_before)
    
    logging.info("Extracting .xml file URL...")
    xml_url, filing_date = get_xml(url)
    
    logging.info("Parsing xml file...")
    xml_table = parse_xml(xml_url)
    
    logging.info("Writing table to .tsv file...")
    write_to_file(xml_table, query_CIK, filing_date, download_path)
    logging.info("Process Completed!")
    
    return

if __name__ == "__main__":
    
    main()