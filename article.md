### A grasp of GraphQL.

GraphQL is a relative new workflow for approaching HTTP-based API development, where the
overall preferred way to implement this kind of APIs has been REST for over two decades. The
way GraphQL presents its approach could arguably mean that in many use cases, it's going to
be the successor of REST, when it comes to developing web-based APIs and clients.

In REST you would generally define different endpoints to expose all your API's functionality,
whereas in GraphQL, you would only define one single entry endpoint through which the server
would handle all client requests. This sole advantage heavily reduces some development burden
like the one encountered in endpoints/routes/urls definition.

As its names implies, GraphQL offers an insanely flexible and accessible *query language*
request constructing mechanism, in which you *query* for the exact data (e.g. model fields)
you require, and also, any other data that could possibly be related to it, and so on
recursively. This represents a huge advantage over the way requests are emitted from clients
in the REST approach, where every request has access to a fixed set of data, and most of the
time, you would have to incur to subsequently consecutive API calls when trying to reach for
related data, given the relative lack of flexibility of REST requests compared to the GraphQL
query-based ones.

GraphQL's ecosystem counts with a ver useful tool, *GraphiQL*, an IDE in the sense that
it allows you to construct your GraphQL requests interactively, with instant feedback on the
available data and required parameters, just like the one you would get from inline
inspections within your text editor or IDE. In this IDE and text editor sense, there are
GraphiQL integrations for some of these, including *JetBrains* IDEs and *VisualCode*.

The GraphQL concept combines both a paradigm and a set of code libraries through which this
paradigm's appliance is achieved. More exactly speaking, GraphQL comprehends the specification
of the concept, the paradigm, and it's through the GraphQL community developed libraries that
you can experience this concept's functionality from both a backend and frontend perspective.
These libraries allow for client-server communication through the use of GraphQL concepts such
as; schema, query, mutation and subscription, formatted by library's target technology
(native language and/or framework) code style.

### Overview.

In this article I'll be presenting some of the core concepts behind GraphQL through a very
usual integration you would implement in your current or next project, an authentication
system, for which I'll be taking a cookie-based approach, since it's a cleaner and more direct
(IMHO), and arguably more secure than its token-based counterpart, since a *secure* and
*HttpOnly* configured cookie adds an extra layer of security to the session token, given
attackers can't access it through javascript code in contrast to the token-based approach,
in which the token is kept in the *localStorage*, where it's directly accessible. There's a
seamlessly token-based integration if you're interested in taking that approach,[check it out
here](https://www.howtographql.com/graphql-python/4-authentication/).

For the backend I'll use Graphene's Django integration, the *graphene-django* library, which
is built upon the code-first approach, meaning you expose all your server functionality
through code, which is translated into GraphQL's schema format, rather than you explicitly
typing the schema, like in the schema-first-approach. A good analogy for this is working with
ORMs (object-relational mappers) against SQL raw queries. For the client, I'll use Vue and
VueApollo, Apollo's Vue integration. Apollo is one of the most popular GraphQL client library,
so if you are using React or Angular, you can easily apply this content, since what I'll be
focusing on, the Apollo client configuration and the query building, don't vary much, if any,
from one Apollo framework distribution to another, and the Vue integration I will be doing is
the minimal to get us going.

This article attempts to offer a detail-rich explanation over the concepts directly related
to the GraphQL workflow and some others encountered around building the authentication
system. In the other hand, I won't be directly explaining code and library syntax, but rather
present a general overview of it, in order to properly articulate with the concepts, so, some
familiarity with the tech stack I just mentioned would be ideal.

### Server

**1.** Django project setup.

Make sure you have the latest versions of *python*, *pip* and *venv* globally installed.
<pre><code># Make and cd into project directory
root:~$ mkdir auth_sys
root:~$ cd auth_sys

# Create a virtual environment where project-level python interpreter and
# dependencies are stored (replace python3 for python in windows)
root:~/auth_sys$ python3 -m venv venv

# Activate the virtual environment to access commands from its context
# venv\Scripts\activate.bat (for windows)
root:~/auth_sys$ source venv/scripts/activate

# Install the needed dependencies
(venv) root:~/auth_sys$ pip install django graphene-django django-cors-headers

# Start a project named the same as the project root directory, 'auth_sys'. Note the trailing '.'
(venv) root:~/auth_sys$ django-admin startproject auth_sys .

# Start and create and app called users
(venv) root:~/auth_sys$ python manage.py startapp users
</code>
</pre>

Add the newly created *users* app the *INSTALLED_APPS* list of you project settings file.
<pre><code># /auth_sys/settings.py
INSTALLED_APPS = [
    ...
    'users',
]
</code>
</pre>

Django comes pre-configured to use a database backend to handle session data by default,
part of this configuration is the *'django.contrib.sessions'* element in *INSTALLED_APPS*
list. As we're going to be taking a cookie-based approach we don't need it, so go ahead and
remove it or comment it out.

Then add the proper session backend, and the CORS and CSRF settings we need:

<pre><code># /auth_sys/settings.py
INSTALLED_APPS = [
    ...
    'corsheaders',
]
MIDDLEWARE = [
    # Add this middleware as high as possible, preferably on top and before *CommonMiddleware*
    'corsheaders.middleware.CorsMiddleware',
    ...
]
# Whitelist the client's origin (we'll configure it to this origin latter)
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8080'
]
# Allow response cookies attachment and request cookies presence
CORS_ALLOW_CREDENTIALS = True
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
</code>
</pre>

**2.** The *User* model.

It's recommended to define a custom user model so that you can easily add fields once you've
created and run the initial migrations. Django provides an abstract class to do this,
*AbstractUser*. Create it in the models module from the recently created *users* app.

<pre><code># /users/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
</code>
</pre>

Then, reference it from the project settings as the new model Django is going to use
to associate all the authentication system with:

<pre><code># /auth_sys/settings.py
...
AUTH_USER_MODEL = 'users.User'
</code>
</pre>

Create the migrations and run them:

<pre><code>python manage.py makemigrations
python manage.py migrate
</code>
</pre>

**3.** Urls.

Open the project's main urls file and replace its content with the following:

<pre><code># /auth_sys/urls.py
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_django.views import GraphQLView

@ensure_csrf_cookie
def csrf_cookie(request):
    return HttpResponse()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf-cookie', csrf_cookie),
    path('graphql/', GraphQLView.as_view())
]
</code>
</pre>

Note of the *csrf-cookie* endpoint, this is what we'll use from our client, for setting the
csrf token the first time the client uses the API. The *csrf_coofiek* function this endpoint
maps to generates the csrf token, thanks to the *ensure_csrf_cookie* decorator, the token
is then attached to the *HttpResponse* in a *Set-Cookie* header.

The *graphql/* endpoint exposes all the API functionality by mapping to the Graphene schema,
This is what we'll use to configure the Apollo client.

**4.** Graphene-Django configuration.

In order to expose our API, we need to define a *schema*,  which is made up of a *Query* and
*Mutation* class, where we define the data we can fetch and the modifications that can be
made upon it respectively.

In Graphene a good way to organize your schema is by having a base *Query* and *Mutation*
classes which will inherit from every app-specific *Query* and *Mutation* classes. Just like
the main urls.py file, where you *include* your app-specific urls.

Define this classes within a schema.py file in your project's directory, the one created with
the *startproject* command.

<pre><code># /auth_sys/schema.py
from graphene import ObjectType, Schema

class Query(ObjectType):
    pass

class Mutation(ObjectType):
    pass

schema = Schema(query=Query, mutation=Mutation)
</code>
</pre>

Now let's reference this *schema* name from the project's settings through the *GRAPHENE*
option, and add *graphene_django* to the *INSTALLED_APPS* list.

<pre><code># /auth_sys/settings.py
...
INSTALLED_APPS = [
    ...
    'graphene_django',
]
...
GRAPHENE = {'SCHEMA': 'auth_sys.schema.schema'}
</code>
</pre>

**5.** Authentication queries and mutations.

Create the *users* app schema with the following content:

<pre><code class="python"># /users/schema.py
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from graphene import Field, Mutation, String
from graphene_django import DjangoObjectType
from users.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class UserMutation(Mutation):
    class Arguments:
        username = String()
        password = String()
    user = Field(UserType)
    def mutate(self, info, username, password):
        pass

class RegisterMutation(UserMutation):
    def mutate(self, info, username, password):
        user = User.objects.create_user(username, password=password)
        login(info.context, user)
        return RegisterMutation(user=user)

class LoginMutation(UserMutation):
    def mutate(self, info, username, password):
        user = authenticate(info.context, username=username, password=password)
        if user:
            login(info.context, user)
        return LoginMutation(user=user)

class LogoutMutation(Mutation):
    user = Field(UserType)
    def mutate(self, info):
        user = info.context.user if info.context.user.is_authenticated else None
        logout(info.context)
        return LogoutMutation(user=user)

class Query(object):
    user = Field(UserType, username=String(required=True))
    authed = Field(UserType)
    def resolve_user(self, info, username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None
    def resolve_authed(self, info):
        user = info.context.user
        # is_authenticated is False for AnonymousUsers
        return user if user.is_authenticated else None

class Mutation(object):
    register = RegisterMutation.Field()
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
</code>
</pre>

Then, from the project schema, let's update the base *Query* and *Mutation* classes
so they inherit from the ones we just created in the *users* app.

<pre><code># /auth_sys/schema.py
import users.schema
...
class Query(ObjectType, users.schema.Query):
...
class Mutation(ObjectType, users.schema.Mutation):
...
</code>
</pre>

So the way this works is, you present your models through Graphene in the form of
*object types*, like the *UserType*, which derives from DjangoObjectType, the Graphene-Django
class that allows the schema creation from your Django models. This *object types* are
mapped through a *root type*, for the *UserType* it would be the *Query* class. An analog
process takes places for the *Mutation* class, where you define a *root mutation* that maps
the specific mutations types like *RegisterMutation*, *LoginMutation* and *LogoutMutation*.

### Client

**1.** Project scaffolding.

Make sure you have the latest versions of node, npm and vue-cli globally installed.

Quickly scaffold a frontend project with Vue's VueCli configuration tool library. From the
project's root directory, do the following:

<pre><code># -n flag for skipping git repo initialization
vue create frontend -n

Vue CLI v4.4.6
? Please pick a preset:
 default (babel, eslint)
❯ Manually select features

# We won't be needing any additional features
# You can toggle them by pressing space
? Check the features needed for your project:
 ◯ Babel
 ◯ TypeScript
 ◯ Progressive Web App ddddd(PWA) Support
 ◯ Router
 ◯ Vuex
 ◯ CSS Pre-processors
 ◯ Linter / Formatter
 ◯ Unit Testing
 ◯ E2E Testing

? Where do you prefer placing config for Babel, ESLint, etc.?
  In dedicated config files
❯ In package.json
</code>
</pre>

**2.** Client configuration.

cd into the newly created *frontend* directory, then, create a vue.config.js file with
the following contents:

<pre><code class="javascript">// /frontend/vue.config.js
module.exports = {
    devServer: {
        // Automatically open a browser tab with the server's domain when it's run
        open: true,
        // The client's local server domain
        host: '127.0.0.1'
    }
}
</code>
</pre>

Install the dependencies the need dependencies:

<pre><code>cd frontend
npm install --save vue-apollo graphql apollo-client apollo-link \
apollo-link-http apollo-cache-inmemory graphql-tag axios js-cookie
</code>
</pre>

Replace the contents of the *main.js* file with the following:

<pre><code class="javascript">// /frontend/src/main.js
import Vue from 'vue'
import App from './App.vue'
import ApolloClient from "apollo-client"
import VueApollo, {ApolloProvider} from 'vue-apollo'
import Cookie from 'js-cookie'
import {createHttpLink} from "apollo-link-http"
import {InMemoryCache} from "apollo-cache-inmemory"
import {ApolloLink, concat} from "apollo-link"

Vue.config.productionTip = false

window.axios = require('axios')
window.axios.defaults.withCredentials = true

function createApp() {
    Vue.use(VueApollo)
    const httpLink = new createHttpLink({
        uri: "http://127.0.0.1:8000/graphql/",
        credentials: 'include',
    })
    const csrfMiddleware = new ApolloLink((operation, forward) => {
        operation.setContext(({headers = {}}) => ({
            headers: {
                ...headers,
                'X-CSRFToken': Cookie.get('csrftoken'),
            }
        }))
        return forward(operation)
    })
    const apolloClient = new ApolloClient({
        link: concat(csrfMiddleware, httpLink),
        cache: new InMemoryCache()
    })
    const apolloProvider = new ApolloProvider({
        defaultClient: apolloClient
    })

    new Vue({
        apolloProvider,
        render: function (h) {
            return h(App)
        },
    }).$mount('#app')
}

if (Cookie.get('csrftoken') === undefined)
    axios.get('http://127.0.0.1:8000/csrf-cookie').then(() => createApp())
else
    createApp()
</code>
</pre>

We wrap the Vue app creation process with a function, so we can fetch the csrf cookie if it
doesn't exist, which is done with an *axios* get request to the endpoint we defined earlier
for fetching the csrf cookie, the token is returned in a *Set-Cookie* http response header,
this tells the client to create or update the cookie with the name and value specified in the
header. This behaviour is not by default though, that's why the axios *setCredentials*,
default option is set to true.

Once the cookie is set (or if it was already), the Vue app is initialized with the
*createApp* function. In there, the Apollo client is configured with the GraphQL server
endpoint, cookie traffic is allowed with *credentials: 'include'* option, which is the mean
all the session system relies on.

Django validates the csrf token getting its value from the request header, so we include it
to the Apollo request headers, but the csrf token is constantly updated (on user
authentication), so we have to be constantly updating its value in the request header as well.
This is done by creating a middleware, some sort inner layer process, that's executed for
every outgoing request. Is in this middleware that we update the *X-CSRFToken* header with the
current csrf cookie value.

This is how the *session* system works:
1. When a user registers or logs in, the server creates a session token with all the session
data but doesn't persist it in any way (thanks to the cookie session backed), it then attaches
this token to the response, as well as a newly generated csrf token, appending one
*Set-Cookie* header for each one of them in the response, these headers contain the name and
value of the cookies so that the client's browser can create and bind them to the client's
domain, which the server must trust as valid origin (the CORS configuration).
2. The session cookie, is sent with every subsequent client's request, allowing the server to
validate user authentication for all your business logic that requires so.
3. When a user logs out, the server invalidates the session token and returns it in the
*Set-Cookie*, the same way as when the user was authenticated, but with an expired timestamp,
triggering the client's browser to delete.
4. Each time a new session is created, so is a new csrf token, which is then attached to the
response and set by the client's browser the same way it's done with the session cookie.

**3.** Client implementation.

Replace all the *App.vue* content with the following:

<pre><code>// /frontend/scr/App.vue
&lt;template>
    &lt;div id="app">
        &lt;div v-if="user">
            &lt;div class="logged">
                &lt;p>{{ user.username }}&lt;/p>
                &lt;button @click="logout">Logout&lt;/button>
            &lt;/div>
        &lt;/div>
        &lt;div v-else>
            &lt;form @submit.prevent="register">
                &lt;fieldset>
                    &lt;legend>Register&lt;/legend>
                    &lt;input v-model="registerUsername" type="text" placeholder="Username" required>
                    &lt;p>{{ registerError }}&lt;/p>
                    &lt;input v-model="registerPassword" type="password" placeholder="Password" required>&lt;br>&lt;br>
                    &lt;input type="submit" value="Register">
                &lt;/fieldset>
            &lt;/form>
            &lt;form @submit.prevent="login">
                &lt;fieldset>
                    &lt;legend>Login&lt;/legend>
                    &lt;input v-model="loginUsername" type="text" placeholder="Username" required>
                    &lt;p>{{ loginError }}&lt;/p>
                    &lt;input v-model="loginPassword" type="password" placeholder="Password" required>&lt;br>&lt;br>
                    &lt;input type="submit" value="Login">
                &lt;/fieldset>
            &lt;/form>
        &lt;/div>
    &lt;/div>
&lt;/template>
&lt;script>
    import gql from 'graphql-tag'
    export default {
        name: 'App',
        apollo: {
            authed: {
                query: gql`query { authed { username } }`,
                update(data) { this.user = data.authed }
            },
            userByUsername: {
                query: gql`query ($username: String!){
                    userByUsername: user(username: $username) { username }
                }`,
                variables() {
                    return {username: this.registerUsername}
                },
                fetchPolicy: 'cache-and-network'
            }
        },
        data: () => ({
            user: null,
            registerUsername: '',
            registerPassword: '',
            loginUsername: '',
            loginPassword: '',
            loginError: '',
        }),
        computed: {
            registerError() {
                return this.userByUsername === null ? '' : 'Username already taken'
            }
        },
        methods: {
            async register() {
                if (this.registerError)
                    return
                await this.$apollo.mutate({
                    mutation: gql`mutation ($username: String!, $password: String!) {
                        register (username: $username, password: $password) {
                            user { username }
                        }
                    }`,
                    variables: {username: this.registerUsername, password: this.registerPassword},
                    update: (store, {data}) => {
                        this.user = data.register.user
                        this.registerUsername = this.registerPassword = ''
                    }
                })
            },
            async login() {
                await this.$apollo.mutate({
                    mutation: gql`mutation ($username: String!, $password: String!) {
                        login (username: $username, password: $password) {
                            user { username }
                        }
                    }`,
                    variables: {username: this.loginUsername, password: this.loginPassword},
                    update: (store, {data}) => {
                        if (data.login.user !== null) {
                            this.user = data.login.user
                            this.loginError = this.loginUsername = ''
                        } else
                            this.loginError = 'Credentials do not match'
                        this.loginPassword = ''
                    }
                })
            },
            async logout() {
                await this.$apollo.mutate({
                    mutation: gql`mutation { logout { user { id }} }`,
                    update:() => { this.user = null }
                })
            }
        }
    }
&lt;/script>
&lt;style>
    form, .logged { width:300px; margin:50px auto; text-align:center; }
&lt;/style>
</code>
</pre>

Appending the *apolloProvider* from within the vue app options allows an *apollo* object to be
used in all Vue components. This object is useful for initializing data attributes out of
GraphQL static queries, dynamically reactive ones by specifying parameters based on
component data attributes or computed properties. In this case there's a clear example for
each one of these behaviours, e.i., the *authed* static query that fetches the currently
authenticated user from the server, it's run only once when the component is created, and the
*userByUsername*, that as its name implies, it queries a User model by its *username*
attribute, which is bind to the query as a parameter that references the component's data
attribute *registerUsername*, we use this to dynamically check whether the register form
username attribute is available, meaning we don't have to submit the form in order to check
for that, instead, we check for the value returned from the reactive query. There's a little
caveat here for the *userByUsername* query and it's the *fetchPolicy* option, there are
several options you can use but I will only explain the one used for this particular example,
*cache-and-network*, what it means is, check the cache where all GraphQL query results are
stored, and return the result if there's a match. Regardless
a match is found on the cache or not, the client then reaches for the *network*, i.e., the
GraphQL server, to update cache with fresh data from the server, and returns it if it wasn't
initially found on the cache. This option is useful when you intend to *mutate* the data
you're also querying, in this case the users. This allows the client to the detect newly
registered users in the register form (username availability), after they've registered and
logged out.

About the mutations; register, login and logout in this case. They are performed through the
mutate method of the *this.$apollo* instance (this is the way you'd do it outside of the
*apollo* object), the options we passed to it are;
1. *mutation*, composed of the arguments it requires follow by the return object and the
desired fields to retrieve.
2. *variables*, an object containing the arguments to the mutation parameters.
3. *update*, a hook fired when the mutation returns, we use it to update the form fields and
error messages accordingly.

### Test

At this point, all that's left is to check the implementation is properly working, so, fire up
both the server's and client's local server with <code>python manage.py runserver</code> and
<code>npm run serve</code> (this one from */frontend* directory) respectively, and navigate to
the client's one (http://127.0.0.1:8080).

After browsing to the client's local server URL open your browser's developer tools (usually
by pressing *F12*), from there check for the following behaviour:
- The first time you visit the site o after you delete all cookies, there's a request
to the *csrf-cookie* endpoint. In its response headers should be the *Set-Cookie* one with its
name and value. If you refresh the site while having this cookie, the request to the
*csrf-cookie* endpoint is not done.
- When you register or login a *sessionid* cookie is created and the *csrftoken* one is
updated with a new value.
- If you refresh while the *sessionid* cookie exists, the user's *username* is displayed with
a logout button.
- When you logout the *sessionid* cookie is deleted.
- While logged out, if you type the *username* of a previously registered user in the register
form you get instant warning without having to submit the form,
- You get a warning in the login form when the credentials don't match, i.e., when a user with
that *username* has not been registered or the password is incorrect.

### Conclusion.

This example covered a very decent amount of what GraphQL server and client implementation has
to offer. What you learned here should suffice you for a wide variety of use cases, but you're
encouraged to keep exploring each concept, so you can make the most out of what's available
out there.

I you're planning to deploy this code to a production environment make sure to properly
configure it to run with a TLS (transport layer security), i.e., with the *https* schema.

It's recommended you implement automated tests covering any variations this authentication
system may encounter in your specific implementation.


### Wrapping up.

If you detect any semantic or typography error I'd appreciate if you notify to this web site's
contact email.
