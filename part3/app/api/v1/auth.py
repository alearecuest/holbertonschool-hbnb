from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

#Gente agrego esta parte nueva
register_model = api.model('Register', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'is_admin': fields.Boolean(description='Is admin user', required=False)
})

@api.route('/register')
class Register(Resource):
    @api.expect(register_model)
    @api.response(201, 'User registered successfully')
    @api.response(400, 'Email already exists or invalid data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        user_data['is_admin'] = user_data.get('is_admin', False)
        
        # Verificamos si el email ya existe
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already exists'}, 400
        
        try:
            # Creamos el usuario, no pepe por favor
            new_user = facade.create_user(user_data)
            
            # Metemos una respuesta sin incluir la contraseña
            user_dict = new_user.to_dict()
            if 'password' in user_dict:
                del user_dict['password']
            
            return user_dict, 201
        except Exception as e:
            return {'error': str(e)}, 400

#Hasta acá agruegue, lo siguiente es lo que ya teníamos
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        credentials = api.payload
        email = credentials['email']
        password = credentials['password']

        user = facade.get_user_by_email(email)

        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
       # token = create_access_token(identity={
        #    'id': str(user.id),
         #   'is_admin': user.is_admin
        #})

        return {'access_token': token}, 200
#Gurises después de leer lo que agregue borren los comentarios porfa