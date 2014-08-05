Extra Marketplace
========================

Módulo para acesso a API do Marketplace do Extra em Python.

Para mais informações sobre a API do Marketplace acesse [http://desenvolvedores.extra.com.br](http://desenvolvedores.extra.com.br/).

## Dependências
- requests - [python-requests.org](http://docs.python-requests.org/en/latest/)

## Exemplos
- SellerItems
```python

>>> import Extra
>>> r = Extra.SellerItems.Items()
>>> r.status_code
200

>>> r.text
u'[{"skuOrigin":"0001","skuId":"123456","defaultPrice":100.0,"salePrice":89.0,
	"availableQuantity":10,"crossDockingTime":0,"installmentId":null,"totalQuantity":10}]'

>>> r.json()
[{u"skuOrigin":u"0001",u"skuId":u"123456",u"defaultPrice":100.0,u"salePrice":89.0,
u"availableQuantity":10,u"crossDockingTime":0,u"installmentId":None,u"totalQuantity":10}]

>>> r.headers
{'content-length': '2323', 'x-powered-by': 'Servlet/2.5 JSP/2.1', 'totalrows': '15',
'keep-alive': 'timeout=60, max=898', 'server': 'Apache', 'date': 'Sat, 02 Aug 2014 20:13:20 GMT',
'content-type': 'application/json; charset=utf-8'}
```

- Loads
```python

>>> import Extra
>>> load = Extra.Loads()
>>> load.AddProduct(skuIdOrigin="1234",sellingTitle="Teste",description="Teste",
brand="Teste",defaultPrice=1.99,salePrice=1.99,categoryList=["Teste>API"],Weight
=1,Length=1,Width=1,Height=1,availableQuantity=10,handlingTime=0,images=[])
[{'skuId': None, 'installmentId': None, 'handlingTime': 0, 'description': 'Teste
', 'Weight': 1, 'EAN': None, 'skuIdOrigin': '1234', 'brand': 'Teste', 'Length':
1, 'Height': 1, 'Width': 1, 'sellingTitle': 'Teste', 'productIdOrigin': None, 's
alePrice': 1.99, 'videos': [], 'images': [], 'defaultPrice': 1.99, 'availableQua
ntity': 10, 'categoryList': ['Teste>API'], 'productUdaLists': []}]

>>> load.Load()
1234
```

## Wiki

Acesse o [wiki](https://github.com/fabiomatavelli/extra-marketplace-python/wiki) para mais informações.