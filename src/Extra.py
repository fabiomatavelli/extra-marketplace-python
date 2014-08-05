#!/usr/env python
# coding=utf-8
__author__ = "Fábio Matavelli <fabiomatavelli@gmail.com>"

import requests
import json
import gzip
from cStringIO import StringIO

class API:
	# Ambiente Sandbox
	sandbox = True
	
	# URL da API (Default None)
	url = None
	
	# Auth e App Token
	authToken = "[seu auth token]"
	appToken = "[seu app token]"
	
	# Cabeçalhos padrões
	headers = {
		"Accept": "application/json"
	}
	
	# Content-types disponíveis
	ctypes = {
		1:"application/json",
		2:"application/gzip",
	}
	
	def __init__(self):
		self.headers["nova-auth-token"] = self.authToken
		self.headers["nova-app-token"] = self.appToken
		if self.sandbox:
			self.url = "https://sandbox.extra.com.br/api/v1"
		else:
			self.url = "https://api.extra.com.br/api/v1"
		
	@classmethod
	def Call(cls,Method,Path,CType=1,**kwargs):
		if CType not in cls().ctypes:
			raise Exception(u"Content-type não encontrado.")
		else:
			cls().headers["Content-type"] = cls().ctypes[CType]
			
		try:
			caller = getattr(requests,Method.lower())
		except AttributeError:
			raise Exception(u"Método '%s' não encontrado" % (Method.lower(),))
		else:
			r = caller("%s/%s" % (cls().url,Path),headers=cls().headers,**kwargs)
			return r
	
	@classmethod
	def get(cls,Path,**kwargs):
		"""Método get da API
		
		Args:
			Path: Caminho da requisição
		"""
		return cls.Call(Method="get",Path=Path,**kwargs)
	
	@classmethod
	def post(cls,Path,CType=1,**kwargs):
		"""Método post da API
		
		Args:
			Path: Caminho da requisição
		"""
		return cls.Call(Method="post",Path=Path,CType=CType,**kwargs)
		
	@classmethod
	def put(cls,Path,**kwargs):
		"""Método put da API
		
		Args:
			Path: Caminho da requisição
		"""
		return cls.Call(Method="put",Path=Path,**kwargs)

class Orders(API):
	@classmethod
	def Status(cls,Status,_startDate=None,_finishDate=None,_offset=1,_limit=50):
		"""Retorna as compras pelo status.
		
		Por padrão, retorna somente 50 registros.
		
		Args:
			Status: O código do status do extra, conforme variável AvailableStatus
			_startDate: Data inicial no formato 2014-01-01T00:00:00.000-03:00
			_finishDate: Data final no formato 2014-01-01T00:00:00.000-03:00
			_offset: Indica a posição inicial de consulta
			_limit: Limita a quantidade de registros trazidos pela consulta
		Returns:
			Retorna o seguinte modelo order conforme documentação do Extra
		Raise:
			Exception: Caso o status não exista no Extra
		"""
		AvailableStatus = ["new","approved","sent","delivered","canceled","partiallyDelivered","sentPartially"]
		
		if Status in AvailableStatus:
			data = {
				"_offset":_offset,
				"_limit":_limit
			}
			
			if _startDate is not None:
				data["_startDate"] = _startDate
				
			if _finishDate is not None:
				data["_finishDate"] = _finishDate
				
			return cls.get("/orders/status/%s" % Status,params=data)
		else:
			raise Exception(u"Status '%s' não encontrado." % Status)
	
	@classmethod
	def New(cls,**kwargs):
		"""Retorna os pedidos cujo status é new
		"""
		return cls.Status(Status="new",**kwargs)
		
	@classmethod
	def Approved(cls,**kwargs):
		"""Retorna os pedidos cujo status é approved
		"""
		return cls.Status(Status="approved",**kwargs)
		
	@classmethod
	def Sent(cls,**kwargs):
		"""Retorna os pedidos cujo status é sent
		"""
		return cls.Status(Status="sent",**kwargs)
		
	@classmethod
	def Delivered(cls,**kwargs):
		"""Retorna os pedidos cujo status é delivered
		"""
		return cls.Status(Status="delivered",**kwargs)
		
	@classmethod
	def Canceled(cls,**kwargs):
		"""Retorna os pedidos cujo status é canceled
		"""
		return cls.Status(Status="canceled",**kwargs)	
		
	@classmethod
	def PartiallyDelivered(cls,**kwargs):
		"""Retorna os pedidos cujo status é partiallyDelivered
		"""
		return cls.Status(Status="partiallyDelivered",**kwargs)
		
	@classmethod
	def SentPartially(cls,**kwargs):
		"""Retorna os pedidos cujo status é sentPartially
		"""
		return cls.Status(Status="sentPartially",**kwargs)
	
	@classmethod
	def Order(cls,orderId,**kwargs):
		"""Retorna uma determinada compra de acordo com o orderId
		
		Args:
			orderId: ID do pedido
		"""
		return cls.get("/orders/%s/" % orderId,**kwargs)
		
	@classmethod
	def OrderItem(cls,orderId,orderItemId,**kwargs):
		"""Retorna o produto de um determinado pedido de acordo com o orderId e o orderItemId
		
		Args:
			orderId: ID do pedido
			orderItemId: ID do produto
		"""
		return cls.get("/orders/%s/orderItems/%s" % (orderId,orderItemId),**kwargs)
		
	@classmethod
	def OrderCancel(cls,orderId,reason,**kwargs):
		"""Cancela uma compra informando uma razão
		
		Args:
			orderId: ID do pedido
			reason: Razão do cancelamento
		"""
		return cls.post("/orders/%s/status/canceled/" % orderId,params={"reason":reason},**kwargs)
		
	@classmethod
	def Tracking(cls,orderId,orderItemId,controlPoint,occurenceDt,carrierName,originDeliveryId,accessKeyNfe,extraDescription=None,url=None,objectId=None,linkNfe=None,nfe=None,serieNfe=None,**kwargs):
		"""Atualiza a informação de entrega de um pedido
		
		Args:
			orderId: ID do pedido
			orderItemId: Lista de IDs dos Itens do pedido, no formato 123-1, onde 123 é o skuId e 1 é a sequência do produto no pedido
			controlPoint: Status do pedido
			occurenceDt: Data da ocorrência
			carrierName: Nome da transportadora
			originDeliveryId: ID de entrega do Lojista. Esse ID deve ser único para um pedido, não podendo haver repetição entre pedidos.
			accessKeyNfe: Número da chave de acesso à nota fiscal. A chave possui 44 dígitos e contém todas as informações da DANFE.
			extraDescription: Descrição adicional sobre tracking
			url: Url para consulta na transportadora.
			objectId: ID do objeto na transportadora
			linkNfe: Url para consulta da NFE
			nfe: Número da Nota Fiscal
			serieNfe: Série da Nota Fiscal
		"""
		
		return cls.post("/orders/%s/ordersItems/trackings/",data=json.loads({
				"orderItemId":orderItemId,
				"controlPoint":controlPoint,
				"extraDescription":extraDescription,
				"occurenceDt":occurenceDt,
				"carrierName":carrierName,
				"url":url,
				"objectId":objectId,
				"originDeliveryId":originDeliveryId,
				"accessKeyNfe":accessKeyNfe,
				"linkNfe":linkNfe,
				"nfe":nfe,
				"serieNfe":serieNfe
			}),**kwargs)
	
class SellerItems(API):
	@classmethod
	def Items(cls,_offset=1,_limit=50,**kwargs):
		"""Recupera todos os produtos que estão associados ao lojista, mesmo os que não estão disponíveis para venda.
		"""
		return cls.get("/sellerItems",params={"_offset":_offset,"_limit":_limit},**kwargs)
		
	@classmethod
	def SellerItem(cls,skuId,defaultPrice,salePrice,availableQuantity,totalQuantity,skuOrigin=None,installmentId=None,crossDockingTime=None,**kwargs):
		"""Associa produtos que já estão disponíveis para venda no Marketplace ao Lojista.
		Através desse serviço, o Lojista informa que também vende um produto que já existe no Marktplace.
		
		Args:
			skuId: SKU ID do produto no Marketplace,
			defaultPrice: Preço "de" no Marketplace,
			salePrice: Preço "por". Preço real de venda,
			availableQuantity: Quantidade disponível para venda
			totalQuantity: Quantidade disponível em estoque,
			skuOrigin: SKU ID do produto no lojista
			installmentId: ID do parcelamento do produto (não está em uso no momento),
			crossDockingTime: Tempo de fabricação
		"""
		return cls.post("/sellerItems",data=json.dumps({
				"skuOrigin":skuOrigin,
				"skuId":skuId,
				"defaultPrice":defaultPrice,
				"salePrice":salePrice,
				"availableQuantity":availableQuantity,
				"installmentId":installmentId,
				"totalQuantity":totalQuantity,
				"crossDockingTime":crossDockingTime
			}),**kwargs)
			
	@classmethod
	def Stock(cls,skuId,availableQuantity,totalQuantity,**kwargs):
		"""Atualiza a quantidade disponível para venda
		
		Args:
			skuId: SKU ID do produto no Marketplace
			availableQuantity: Quantidade disponível para venda,
			totalQuantity: Quantidade disponível em estoque
		"""
		return cls.put("/sellerItems/%s/stock" % skuId,data=json.dumps({
				"availableQuantity":availableQuantity,
				"totalQuantity":totalQuantity
			}),**kwargs)
			
	@classmethod
	def Prices(cls,skuId,defaultPrice,salePrice,installmentId=None,**kwargs):
		"""Atualiza o preço do produto para venda
		
		Args:
			skuId: SKU ID do produto no Marketplace
			defaultPrice: Preço 'de',
			salePrice: Preço 'por',
			installmentId: ID do parcelamento do produto
		"""
		return cls.put("/sellerItems/%s/prices" % skuId,data=json.dumps({
				"defaultPrice":defaultPrice,
				"salePrice":salePrice,
				"installmentId":installmentId
			}),**kwargs)
	
	@classmethod
	def Sku(cls,skuId,**kwargs):
		"""Recupera a informação de um determinado SKU através do SKU ID do Marketplace
		
		Args:
			skuId: SKU ID do produto no Marketplace
		"""
		return cls.get("/sellerItems/%s" % skuId,**kwargs)
	
	@classmethod
	def SkuOrigin(cls,skuOrigin,**kwargs):
		"""Recupera a informação de um determinado SKU através do SKU ID do Lojista
		
		Args:
			skuOrigin: SKU ID do Lojista
		"""
		return cls.get("/sellerItems/skuOrigin/%s" % skuOrigin,**kwargs)
		
	@classmethod
	def Selling(cls,_offset=1,_limit=50,**kwargs):
		"""Recupera apenas os produtos do Lojista que estão disponíveis para venda.
		
		Args:
			_offset: Indica a posição inicial de consulta
			_limit: Limita a quantidade de registros trazidos pela consulta
		"""
		return cls.get("/sellerItems/status/selling",**kwargs)

class Loads(API):
	# Armazenda os produtos utilizando o AddProduct
	__products = []
	
	@classmethod
	def AddProduct(cls,skuIdOrigin,sellingTitle,description,brand,defaultPrice,salePrice,categoryList,Weight,Length,Width,Height,availableQuantity,handlingTime,images,videos=[],productUdaLists=[],skuId=None,productIdOrigin=None,EAN=None,installmentId=None):
		"""Adiciona um produto à variável __products para ser utilizada pelo método Load.
		
		Args:
			skuIdOrigin (string): SKU ID do produto do lojista,
			skuId (string, optional): SKU ID do produto no Marketplace - utilizado para realizar associação de produtos,
			productIdOrigin (string, optional): ID do produto do lojista para fazer o agrupamento de SKUs,
			sellingTitle (string): Nome no Marketplace. Ex Televisor de LCD Sony Bravia 40”...,
			description (string): Descrição do produto. Aceita tags HTML para formatar a apresentação da descrição, no entanto há alguma
			tags restritas (tags para acesso a conteúdo externo):img, object, script e iframe.,
			brand (string): Marca. Ex Sony,
			EAN (string, optional): Código EAN do produto (código de barras),
			defaultPrice (double): Preço “de” no Marketplace. Não pode ser 0 (zero) e deve ter no máximo duas casas decimais,
			salePrice (double): Preço “por”. Preço real de venda. Não pode ser 0 (zero) e deve ter no máximo duas casas decimais,
			categoryList (List[string]): Lista de categorias. Quantidade máxima de cinco (5) níveis de categoria por produto.,
			productUdaLists (List[productUdas]): Lista de atributos do Produto. Quantidade máxima de 38 atributos por produto.,
			Weight (double): Peso do produto, em quilos. Não pode ser 0 (zero) e deve ter no máximo duas casas decimais,
			Length (double): Comprimento do produto, em metros. Não pode ser 0 (zero) e deve ter no máximo duas casas decimais,
			Width (double): Largura do produto, em metros. Não pode ser 0 (zero) e deve ter no máximo duas casas decimais,
			Height (double): Altura do produto, em metros. Não pode ser 0 (zero) e deve ter no máximo duas casas decimais,
			availableQuantity (int): Quantidade disponível,
			handlingTime (int): Tempo de fabricação em dias (padrão é 0),
			installmentId (int, optional): ID do parcelamento,
			videos (List[string], optional): Lista de URLs de vídeos. Quantidade máxima de dois (2) vídeos por produto.,
			images (List[string]): Lista de URLs de imagens. Pelo menos uma imagem precisa ser informada. Quantidade máxima de quatro (4) imagens por produto.
		"""
		for product in cls.__products:
			if product["skuIdOrigin"] == skuIdOrigin:
				raise Exception("Produto '%s' ja existe na lista de produtos para carga." % (skuIdOrigin,))
		
		cls.__products.append({
			"skuIdOrigin":skuIdOrigin,
			"skuId":skuId,
			"productIdOrigin":productIdOrigin,
			"sellingTitle":sellingTitle,
			"description":description,
			"brand":brand,
			"EAN":EAN,
			"defaultPrice":defaultPrice,
			"salePrice":salePrice,
			"categoryList":categoryList,
			"productUdaLists":productUdaLists,
			"Weight":Weight,
			"Length":Length,
			"Width":Width,
			"Height":Height,
			"availableQuantity":availableQuantity,
			"handlingTime":handlingTime,
			"installmentId":installmentId,
			"videos":videos,
			"images":images
			})
			
		return cls.__products
	
	@classmethod
	def ClearProducts(cls):
		"""Limpa a lista de produtos __products
		"""
		cls.__products = []
	
	@classmethod
	def DelProduct(cls,skuIdOrigin):
		"""Deleta um produto da lista de acordo com o skuIdOrigin
		"""
		for key,product in enumerate(cls.__products):
			if product["skuIdOrigin"] == skuIdOrigin:
				del(cls.__products[key])
		else:
			raise Exception(u"Produto '%s' não encontrado." % (skuIdOrigin,))
			
		return cls.__products
		
	@classmethod
	def GetProducts(cls):
		"""Retorna a lista de produtos
		
		Return:
			Retorna a lista de produtos __products
		"""
		
		return cls.__products
	
	@classmethod
	def Load(cls,**kwargs):
		"""Realiza a carga dos produtos armazenados no __products
		
		Return:
			Retorna o ID da carga
		"""
		
		# Compacta o json do __products
		stream = StringIO()
		with gzip.GzipFile(fileobj=stream,mode="wb") as compress:
			compress.write(json.dumps(cls.__products))
		
		r = cls.post("/loads/products",data=stream.getvalue(),CType=2,**kwargs)
		if r.status_code == 201:
			l = r.headers["location"].split("/")
			return l[-1]
		else:
			error = r.json()
			raise Exception(error["errorDesc"],error["errorCode"])
	
	@classmethod
	def ImporterInfo(cls,importerInfoId,**kwargs):
		"""Consulta o status da carga dos produtos.
		"""
		
		return cls.get("/loads/products/%s" % (importerInfoId,),**kwargs)
	
	@classmethod
	def ImporterInfoSku(cls,importerInfoId,skuOrigin,**kwargs):
		"""Consulta a informação de um produto carregado através da operação de importação
		"""
		return cls.get("/loads/products/%s/%s" % (importerInfoId,skuOrigin),**kwargs)
	
if __name__ == "__main__":
	pass
