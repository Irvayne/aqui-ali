from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):

	nome = forms.CharField(required=True)
	login = forms.CharField(required=True)
	email = forms.CharField(required=True)
	senha = forms.CharField(required=True)
	confirmacao = forms.CharField(required=True)

	def is_valid(self):
		valid = True

		if self.data['senha'] != self.data['confirmacao']:
			self.adiciona_erros('Senhas nao compativeis')
			return False

		if not super(RegistrarUsuarioForm, self).is_valid():
			self.adiciona_erros('Por favor, verifique os dados informados')
			valid = False

		user_exists = User.objects.filter(username=self.data['login']).exists()

		if user_exists:
			self.adiciona_erros('Usuario com esse login ja existe')
			valid = False

		return valid


	def adiciona_erros(self, message):
		self.full_clean()
		errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
		errors.append(message)