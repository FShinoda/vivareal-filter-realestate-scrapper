# COLE SEU LINK PERSONALIZADO AQUI, ENTRE AS ASPAS
URL = "https://www.vivareal.com.br/aluguel/sp/sao-paulo/zona-sul/vila-mariana/apartamento_residencial/2-quartos/#onde=Brasil,S%C3%A3o%20Paulo,S%C3%A3o%20Paulo,Zona%20Sul,Vila%20Mariana,,,,BR%3ESao%20Paulo%3ENULL%3ESao%20Paulo%3EZona%20Sul%3EVila%20Mariana,,,&preco-ate=3700&preco-total=sim&quartos=2"

# NÃO MEXA DAQUI PARA BAIXO ########################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# CONSTS
PATH = (os.path.dirname(os.path.abspath(__file__))) + '\\'
APARTMENTS_ALLOWLIST = PATH + 'apartmentList.txt'
APARTMENTS_BLOCKLIST = PATH + 'apartmentBlockList.txt'

# FUNCTIONS
def diffList(mainList, diffList):
  return [i for i in mainList if i not in diffList]

def removeListDuplicates(myList):
  return list(set(myList))

def scrapApartments():
  apartmentsList = []
  driver = webdriver.Chrome()
  driver.get(URL)

  while True:
    try:
      WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CLASS_NAME, 'hbs-filters__pill')) > 1
      )

      time.sleep(4)

      resultsSection = driver.find_element(By.CLASS_NAME, 'results-main__panel')

      for link in resultsSection.find_elements(By.TAG_NAME, 'a'):
        print(link.get_attribute('href'))
        apartmentsList.append(link.get_attribute('href'))

      nextPageElement = driver.find_elements(By.CLASS_NAME, "pagination__item")[-1]

      buttonNextPage = nextPageElement.find_element(By.TAG_NAME, "button")
            
      if buttonNextPage.get_attribute("data-disabled") != None:
          print("Next Page button is disabled. Exiting the loop.")
          break

      ActionChains(driver).move_to_element(buttonNextPage).click().perform()

      WebDriverWait(driver, 10).until(
          EC.staleness_of(nextPageElement)
      )

    except Exception as e:
      print(f"An error occurred: {e}")
      break
  
  driver.quit()
  return apartmentsList

def saveFilteredApartments(newApartmentsList):
  apartmentsBlockList = []
  apartmentsFilterList = []
  with open(APARTMENTS_BLOCKLIST, 'r') as file:
    for line in file:
      apartmentsBlockList.append(line.strip())

  apartmentsFilterList = diffList(removeListDuplicates(newApartmentsList), removeListDuplicates(apartmentsBlockList))

  with open(APARTMENTS_ALLOWLIST, 'w') as file:
    for ap in apartmentsFilterList:
      file.write(ap + '\n')

# MAIN
newApartmentsList = scrapApartments()
saveFilteredApartments(newApartmentsList)