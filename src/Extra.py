#!/usr/env python
# coding=utf-8
__author__ = "Fábio Matavelli <fabiomatavelli@gmail.com>"

import requests
import json

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
	def post(cls,Path,**kwargs):
		"""Método post da API
		
		Args:
			Path: Caminho da requisição
		"""
		return cls.Call(Method="post",Path=Path,**kwargs)
		
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
			}))
	
class SellerItems(API):
	@classmethod
	def Items(cls,_offset=1,_limit=50,**kwargs):
		"""Recupera todos os produtos que estão associados ao lojista, mesmo os que não estão disponíveis para venda.
		"""
		return cls.get("/sellerItems",params={"_offset":_offset,"_limit":_limit},**kwargs)
