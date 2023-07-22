from django.test import TestCase

# def index(request):
#     if "REG" in request.GET:
#         if is_valid_phone_number(str(request.GET.get('REG'))):
#             user_phone = request.GET['REG']
#             # Проверяем, существует ли пользователь с таким номером телефона
#             try:
#                 # user = User.objects.get(username=user_phone)
#                 user = authenticate(request, username=user_phone, backend=LoginBackend)
#                 print('backend')
#                 if user is not None:
#                     print('Авторизуем')
#                     # Авторизуем пользователя в системе
#                     login(request, user)
#                 return redirect('lk')
#             except CustomUser.DoesNotExist:
#                 # Если пользователя нет, то создаем нового пользователя
#                 user = CustomUser.objects.create_user(
#                     username=user_phone,
#                 )
#                 print('except')
#                 user.save()
#             if user is not None:
#                 print('Авторизуем')
#                 # Авторизуем пользователя в системе
#                 login(request, user)
#             return redirect('lk')
#
#     if "TOPPING" in request.GET:
#         results = request.GET
#         create_order(results)
#         add_user(results)
#     return render(request, 'index.html')
#
# <aside class="modal fade" id="RegModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="RegModalLabel" aria-hidden="true">
# 			<div class="modal-dialog modal-dialog-centered">
# 				<div class="modal-content px-4 cake__modal">
# 					<div class="modal-header border-0 pb-0 pt-4">
# 						<button @click="Reset" type="button" class="btn-close border rounded-pill" data-bs-dismiss="modal" aria-label="Close"></button>
# 					</div>
# 					<div class="modal-header border-0 py-0">
# 						<label for="reg" class="modal-title font_Gogh fs_40 cake_blue" id="RegModalLabel">Вход / Регистрация</label>
# 					</div>
# 					<form class="d-none" >
# 						<input v-model="RegInput" type="text" name="REG">
# 						<button type="submit" ref="HiddenFormSubmitReg">reg</button>
# 					</form>
# 					<v-form :validation-schema="RegSchema" class="modal-body position-relative d-flex flex-column align-items-center px-5 pb-4" @submit="RegSubmit">
# 						<v-field v-if="RegInput !== 'Регистрация успешна'" v-model="RegInput" name="reg" type="text" id="reg" :placeholder="Step === `Number` ? `Введите ваш номер` : `Введите код`" class="form-control cake__textinput"></v-field>
# 						<v-field v-if="Step === 'Number'" v-model="RegInput" type="phone" name="phone_format" class="d-none"></v-field>
# 						<v-field v-if="Step === 'Code'" v-model="RegInput" type="phone" name="code_format" class="d-none"></v-field>
# 						<button v-if="RegInput !== 'Регистрация успешна'" type="submit" class="btn text-white w-100 rounded-pill mt-3 py-2 shadow-none cake__button fs_12 cake__bg_pink">Отправить</button>
# 						<span v-if="RegInput === 'Регистрация успешна'" class="cake_grey text-center">Регистрация успешна</span>
# 						<small class="fs_12 cake_pink text-center position-absolute bottom-0"><error-message name="reg">
# 							<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-exclamation-circle mb-1" viewBox="0 0 16 16">
# 								<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
# 								<path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
# 							</svg>
# 							{% verbatim %}{{Step === 'Number' ? 'Введите номер' : 'Введите код'}}{% endverbatim %}</error-message></small>
# 						<error-message name="phone_format" class="fs_12 cake_pink text-center position-absolute bottom-0"></error-message>
# 						<error-message name="code_format" class="fs_12 cake_pink text-center position-absolute bottom-0"></error-message>
# 					</v-form>
#
# 					<div class="modal-footer d-flex flex-column justify-content-between align-items-center text-center border-0 mx-5">
# 						<p class="fs_12 cake_grey">{% verbatim %}{{Step === `Number` ? `Нажимая на кнопку, вы соглашаетесь на обработку персональных данных в соответствии с <a class="text fs_12 cake_blue" href="{% url 'agreement' %}">политикой конфиденциальности</a>` : Step === 'Code' ? `Осталось времени: 05:00` : ``}}{% endverbatim %}</p>
# 						<a href="#" v-if="Step === `Code`" @click.prevent="ToRegStep1" class="text-decoration-none cake_pink fs_12">изменить данные</a>
# 					</div>
# 				</div>
# 			</div>
# 		</aside>
#
# Vue.createApp({
#     components: {
#         VForm: VeeValidate.Form,
#         VField: VeeValidate.Field,
#         ErrorMessage: VeeValidate.ErrorMessage,
#     },
#     data() {
#         return {
#             RegSchema: {
#                 reg: (value) => {
#                     if (value) {
#                         return true;
#                     }
#                     return 'Поле не заполнено';
#                 },
#                 phone_format: (value) => {
#                     const regex = /^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$/
#                     if (!value) {
#                         return true;
#                     }
#                     if ( !regex.test(value)) {
#
#                         return '⚠ Формат телефона нарушен';
#                     }
#                     return true;
#                 },
#                 code_format: (value) => {
#                     const regex = /^[a-zA-Z0-9]+$/
#                     if (!value) {
#                         return true;
#                     }
#                     if ( !regex.test(value)) {
#
#                         return '⚠ Формат кода нарушен';
#                     }
#                     return true;
#                 }
#             },
#             Step: 'Number',
#             RegInput: '',
#             EnteredNumber: ''
#         }
#     },
#     methods: {
#         RegSubmit() {
#             if (this.Step === 'Number') {
#                 this.$refs.HiddenFormSubmitReg.click()
#                 this.Step = 'Code'
#                 this.EnteredNumber = this.RegInput
#                 this.RegInput = ''
#             }
#             else {
#                 this.$refs.HiddenFormSubmitReg.click()
#                 this.Step = 'Finish'
#                 this.RegInput = 'Регистрация успешна'
#             }
#         },
#         ToRegStep1() {
#             this.Step = 'Number'
#             this.RegInput = this.EnteredNumber
#         },
#         Reset() {
#             this.Step = 'Number'
#             this.RegInput = ''
#             EnteredNumber = ''
#         }
#     }
# }).mount('#RegModal')
