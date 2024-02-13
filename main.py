from cryptoData import cryptoData
from mongoDBUtils import mongoProject

cd = cryptoData(True)
data = cd.getTopVolatileProducts()
print(data)

cryptoProject = mongoProject()
cryptoProject.setCollection("crypto_analytics", "test_collection")
cryptoProject.deleteData()
cryptoProject.insertData(data)
cryptoProject.printCollection()
