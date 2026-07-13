# Technical Documentation - Study Manager

Este documento registra o histórico de evoluções e funcionalidades do Study Manager, um projeto desenvolvido como Capstone do curso CS50W. A documentação segue uma estrutura baseada em commits semânticos, detalhando as alterações incrementais realizadas na base do sistema.

Estrutura de Commits
A mensagem segue o formato: <tipo>(<escopo opcional>): <descrição>

Exemplo:  
`feat(auth): configure authentication URL patterns`

Para ler e se aprofundar mais nos commits semânticos , aqui estão as URLS que é possível ler e entender mais do assunto

https://www.conventionalcommits.org/pt-br/v1.0.0-beta.4/#especifica%c3%a7%c3%a3o

https://dev.to/diegobrandao/padronizando-commits-git-com-um-script-bash-uma-solucao-simples-para-um-problema-comum-2bdl

https://dev.to/diegobrandao/padronizando-commits-git-com-um-script-bash-uma-solucao-simples-para-um-problema-comum-2bdl

<hr>

# feat(auth): configure authentication URL patterns

- **Importações**: Carrega as ferramentas de roteamento (`path`), as views de autenticação prontas do Django (`auth_views`) e as views personalizadas da sua aplicação (`. import views`).
- **`urlpatterns`**: Lista que mapeia rotas HTTP para funções ou classes Python.
- **Rotas**:
  - `""`: Mapeia a URL base (`/`) para a função `dashboard` em `views.py`.
  - `"login/"`: Utiliza a classe `LoginView` nativa do Django, injetando o template `login.html`.
  - `"logout/"`: Utiliza a classe `LogoutView` nativa do Django para encerrar a sessão.
  - `"register/"`: Mapeia a URL para a função `register` em `views.py`.
- **`name`**: Atribui um identificador (apelido) à rota, permitindo que você use `{% url 'nome' %}` nos seus templates sem precisar alterar o caminho caso a URL mude.

<span style="color:rgb(0, 176, 240)">auth<i>views.LoginView.as</i>view()</span> converte uma **Classe de View** do Django em uma **Função de View** (o formato que o `urls.py` espera).

- **O que é**:
  - `LoginView` é uma classe pronta do Django que encapsula toda a lógica de login (validar usuário/senha, criar sessão, redirecionar em caso de erro).
- **O que o `.as_view()` faz**:
  - Como o roteamento do Django (o arquivo `urls.py`) funciona através de funções que recebem uma requisição (`request`), o método `.as_view()` retorna uma função "wrapper" que, ao ser chamada:
    1. Instancia a classe `LoginView`.
    2. Configura a requisição atual.
    3. Executa os métodos necessários (como `get` para renderizar o formulário ou `post` para processar o login).
    4. Retorna a resposta HTTP final.

<hr>

# feat(models): create Subject model

**models**: Definição da estrutura de dados para matérias de estudo.

- `user`: Relacionamento 1:N com o usuário (`ForeignKey`), garantindo exclusão em cascata (`CASCADE`).
- `name`: Campo de texto para o nome da matéria.
- `description`: Campo de texto opcional para detalhes.
- `color`: Armazena o código hexadecimal da cor associada à matéria (padrão: `#5B88A5`).
- `created_at`: Data de criação automática.
- **Metadados**: Ordenação padrão por nome (`Meta.ordering`).
- **Método `__str__`**: Retorno amigável contendo o nome da matéria e o usuário proprietário.

<hr>

# feat(models): create Topic model

**models**: Definição da estrutura de dados para tópicos de estudo vinculados a uma matéria.

- `subject`: Relacionamento 1:N com o modelo `Subject` (`ForeignKey`), com exclusão em cascata.
- `name`: Nome do tópico.
- `notes`: Campo de texto para anotações detalhadas.
- `is_completed`: Flag booleana para marcar progresso.
- `order`: Campo inteiro para controle de ordenação manual.
- `created_at`: Data de criação automática.
- **Metadados**: Ordenação composta por prioridade (`order`) e data (`created_at`).
- **Método `__str__`**: Identificação clara do tópico e sua matéria pai.

<hr>

# feat(models): create PomodoroSession

- **models**: Definição da estrutura de dados para o registro de sessões de foco (Pomodoro).
  - `user`: Relacionamento 1:N com o usuário.
  - `subject`: Relacionamento 1:N com a matéria associada à sessão.
  - `started_at`: Data e hora de início da sessão.
  - `duration_minutes`: Duração da sessão em minutos (padrão: 25).
  - `completed`: Flag booleana para status da sessão.
  - **Metadados**: Ordenação decrescente por data de início (`-started_at`).
  - **Método `__str__`**: Exibição formatada com status (ícone) e data.

<hr>

# feat(models): implement busciness logic methods for subject model

- **`progress()`**:
  - **Finalidade**: Quantificar o desempenho acadêmico do usuário em uma matéria específica.
  - **Lógica**:
    1. `topics = self.topics.all()`: Utiliza o `related_name` definido anteriormente para acessar todos os tópicos vinculados à matéria.
    2. **Validação**: `if not topics.exists(): return 0` previne o erro de divisão por zero (caso a matéria esteja vazia).
    3. **Cálculo**: Filtra apenas os tópicos com `is_completed=True`, conta-os e divide pelo total. O resultado é multiplicado por 100 e convertido para `int` para exibição percentual.
- **`total_study_minutes()`**:
  - **Finalidade**: Agregação de dados temporais para métricas de produtividade.
  - **Lógica**:
    1. `sessions = self.pomodoro_sessions.filter(completed=True)`: Seleciona apenas as sessões de Pomodoro finalizadas.
    2. **Agregação**: Utiliza uma _list comprehension_ dentro da função `sum()` para somar o atributo `duration_minutes` de cada instância encontrada.

<hr>

# feat(models): create Flashcard model

- **models**: Definição da estrutura para cartões de memória.
  - `subject`: Relacionamento 1:N com a matéria.
  - `front` / `back`: Conteúdo (pergunta e resposta).
  - `next_review_date`: Data da próxima revisão (default: data atual).
  - `interval_days`: Intervalo de dias entre revisões (default: 1).
  - `__str__` (com `:50`): Corta de string que limita a exibição do `front` a 50 caracteres para manter a interface limpa.
  - `is_due_today()`: Validador booleano que compara `next_review_date` com a data atual. Retorna `True` se a revisão for necessária hoje ou se o cartão estiver atrasado.
- **Algoritmo de Revisão - `apply_review(rating)`**:
  - **Objetivo**: Implementar o sistema de **Repetição Espaçada (SRS)**, que ajusta dinamicamente quando você verá o cartão novamente com base na sua performance:
    - **`easy`**: O usuário dominou o conteúdo. O intervalo atual é dobrado (mínimo de 7 dias) para que o cartão volte a aparecer apenas no futuro distante.
    - **`hard`**: O usuário teve dificuldade. O intervalo é mantido ou ajustado para 2 dias, forçando uma revisão mais próxima.
    - **`wrong`**: O usuário errou. O intervalo é resetado para 1 dia, reiniciando o ciclo de aprendizado.
  - **Persistência**: Após definir o novo `interval_days`, o método calcula a `next_review_date` somando o novo intervalo à data atual e executa `self.save()` para persistir a alteração no banco de dados imediatamente.
- **`self.next_review_date`**
  - **`date.today()`**: Pega a data de hoje (baseada no calendário do sistema).
- **`timedelta(days=self.interval_days)`**: Cria um "delta" (uma diferença de tempo). Se `interval_days` for 7, isso representa um intervalo de exatamente 7 dias.
- **A soma (`+`)**: O Django/Python permite somar uma data com um `timedelta`. O resultado é uma nova data, exatamente `X` dias no futuro.
- **Atribuição**: O resultado dessa conta é salvo no campo `next_review_date`, que é o campo que o seu sistema usa para saber quando aquele cartão deve "aparecer" novamente para o usuário.
- **Metadados**: Ordenação por prioridade (`next_review_date`), garantindo que os cartões atrasados apareçam primeiro no fluxo de estudo.

<hr>

# feat(models): create FlashcardReview

- **models**: Definição da estrutura que registra o histórico de cada revisão realizada em um `Flashcard`.
  - `RATING_CHOICES`: Enumeração das opções de avaliação (`easy`, `hard`, `wrong`), garantindo integridade dos dados através de uma lista de escolhas fixas.
  - `flashcard`: Relacionamento 1:N com o modelo `Flashcard`, permitindo rastrear o histórico completo de desempenho de cada cartão.
  - `rating`: Campo de caracteres que armazena a avaliação selecionada pelo usuário.
  - `reviewed_at`: Data e hora exatas da revisão, preenchidas automaticamente (`auto_now_add`).
  - **Método `__str__`**: Representação textual do log, incluindo o cartão, a nota recebida e a data, facilitando a visualização no painel administrativo.
  - **Metadados**: Ordenação por ordem cronológica decrescente (`-reviewed_at`), exibindo sempre as revisões mais recentes no topo da lista.

### Por que criar este modelo?

Diferente do modelo `Flashcard` que guarda o **estado atual** (quando ver o cartão novamente), o `FlashcardReview` guarda o **histórico de esforço**. Com essa estrutura, você pode no futuro gerar gráficos de progresso, calcular a taxa de acerto por matéria ou identificar quais cartões você tem mais dificuldade de memorizar.

<hr>

# feat(models): create WeeklyGoal

- - `subject`: Relacionamento com a matéria alvo.
    - `target_hours`: Meta de horas a serem cumpridas na semana (campo `FloatField`).
    - `week_start`: Data de início da semana (deve ser sempre uma segunda-feira).
    - **`current_hours()`**: Método que calcula o progresso real. Filtra as sessões de `PomodoroSession` concluídas dentro do intervalo de 7 dias a partir de `week_start`, converte a soma dos minutos para horas e arredonda para uma casa decimal.
    - **`percentage()`**: Calcula o progresso percentual atingido, com trava de limite em 100% para evitar exibição de valores superiores caso o usuário ultrapasse a meta.
- **Metadados e Integridade**:
  - `ordering`: Ordena por data e matéria.
  - `unique_together`: Impede a criação de múltiplas metas para a mesma matéria, pelo mesmo usuário, na mesma semana, garantindo consistência dos dados.

### Observações Técnicas

- **Filtro por `range`**: A lógica em `current_hours()` utiliza `started_at__date__range` para isolar exatamente a semana da meta. Isso permite que o sistema saiba, em tempo real, quanto falta para atingir o objetivo da semana corrente.
- **Validação de Negócio**: O `unique_together` é a "chave" para evitar inconsistências, garantindo que cada meta semanal seja única e fácil de consultar pela interface.

<hr>

# feat(urls): configure CRUD URL patterns for Subject model

- **urls**: Mapeamento dos endpoints para o CRUD (Create, Read, Update, Delete) do modelo `Subject`:
  - `subjects/`: Lista todas as matérias (`subjects_list`).
  - `subjects/new/`: Formulário para criar uma nova matéria (`subject_create`).
  - `subjects/<int:pk>/`: Detalhes de uma matéria específica identificada pela sua Primary Key (`subject_detail`).
  - `subjects/<int:pk>/edit/`: Edição de uma matéria existente (`subject_edit`).
  - `subjects/<int:pk>/delete/`: Remoção de uma matéria (`subject_delete`).

### Observação Técnica

- **`<int:pk>`**: É um **path converter**. Ele instrui o Django a capturar o valor após a barra como um número inteiro (`int`) e passá-lo para a view correspondente como o argumento `pk` (Primary Key). Isso é o padrão para identificar instâncias específicas de modelos no banco de dados.

https://docs.djangoproject.com/en/6.0/topics/http/urls/ - Dispatcher
https://codingnomads.com/what-is-path-converter - Patch Converter

<hr>

# feat(urls): add URL patterns for Topic

- **urls**: Mapeamento dos endpoints para manipulação de tópicos via API:
  - `topics/new/`: Endpoint para criação de um novo tópico (`topic_create`).
  - `topics/<int:pk>/toggle/`: Endpoint para alternar o status de conclusão (`is_completed`) de um tópico específico (`topic_toggle`).
  - `topics/<int:pk>/delete/`: Endpoint para remoção de um tópico (`topic_delete`).

### Observação Técnica

- **`toggle`**: Esta rota é desenhada para interações via JavaScript (fetch/AJAX). Em vez de renderizar uma página completa, este endpoint normalmente apenas atualiza o banco de dados e retorna uma resposta JSON confirmando o novo status (`True` ou `False`), permitindo que a interface do usuário seja atualizada dinamicamente sem recarregar a página.

<hr>

# feat(urls): add URL patterns for Flashcard

- - `flashcards/`: Exibe a lista de todos os cartões (`flashcard_list`).
    - `flashcards/new/`: Formulário de criação de novo cartão (`flashcard_create`).
    - `flashcards/review/`: Inicia uma sessão de estudo baseada na repetição espaçada (`flashcard_review_session`).
    - `flashcards/<int:pk>/delete/`: Remove um cartão específico (`flashcard_delete`).
    - `flashcards/<int:pk>/submit/`: Endpoint de processamento para submeter a avaliação (`easy`, `hard`, `wrong`) de uma revisão (`flashcard_submit_review`).

### Observação Técnica

- **`flashcard_review` vs `flashcard_submit`**: A separação entre esses endpoints é de sua extrema importância . Enquanto `review` prepara o contexto para o usuário estudar, o `submit` atua como um endpoint de API que recebe os dados do formulário/interação do usuário, executa a lógica de cálculo do SRS (`apply_review`) e redireciona ou retorna a confirmação de atualização do estado do cartão.

<hr>

# feat(urls): add URL patterns for Pomodoro

- **urls**: Mapeamento dos endpoints para o sistema de foco (timer):
  - `pomodoro/`: Carrega a interface principal do temporizador Pomodoro (`pomodoro`).
  - `pomodoro/save/`: Endpoint para persistir o registro da sessão no banco de dados após o término do tempo (`pomodoro_save`).

### Observação Técnica

- **Separação de responsabilidades**: O endpoint `pomodoro` renderiza a página de trabalho, enquanto o `pomodoro_save` atua como um _callback_ (geralmente via `POST` request disparado pelo JavaScript ao final dos 25 minutos). Isso garante que o registro da sessão no banco de dados ocorra de forma assíncrona, mantendo a integridade dos seus dados de produtividade sem a necessidade de recarregar a interface.

<hr>

# feat(urls): add URL patterns for Goals

- **urls**: Mapeamento dos endpoints para o gerenciamento de `WeeklyGoal`:
  - `goals/`: Exibe o painel com as metas semanais cadastradas (`goals_list`).
  - `goals/new/`: Formulário para definir uma nova meta de horas de estudo (`goal_create`).
  - `goals/<int:pk>/delete/`: Remoção de uma meta específica (`goal_delete`).

### Observação Técnica

- **Gestão de Metas**: Estas rotas permitem o controle do ciclo de vida das metas. Ao utilizar `pk` na rota de deleção, o sistema garante que apenas a meta específica daquela matéria e semana seja removida, mantendo a integridade dos históricos de estudo que possam ter sido registrados anteriormente.

<hr>

# feat(urls): add URL patterns for Dashboard

- **urls**: Mapeamento do endpoint para monitoramento de desempenho:
  - `dashboard/activity/`: Acessa a view `dashboard_activity`, responsável por compilar e exibir os dados agregados das sessões de estudo, progresso de tópicos e metas alcançadas.

### Observação Técnica

- **Analytics do Sistema**: Este endpoint centraliza a lógica de leitura de dados. Diferente das outras rotas que gerenciam entidades individuais (CRUDS), esta rota serve como uma **View de Resumo**, onde você provavelmente consome os métodos de cálculo que definimos nos modelos (`progress()`, `current_hours()`, etc.) para gerar visualizações de progresso para o usuário.

# -----------------------><span style="color:rgb(255, 255, 0)">VIEWS</span> <--------------------------

# feat(views): create initial view stubs for all application endpoints

**views**: Implementação da estrutura inicial (boilerplate) para todas as funções da aplicação.

- **Objetivo**: Estabelecer o contrato entre as URLs definidas e a lógica de negócio, garantindo que o servidor Django inicie sem erros de importação (`ImportError` ou `AttributeError`).
- **Implementação**: Criação de funções básicas para todos os módulos (Auth, Subjects, Topics, Flashcards, Pomodoro, Goals e Analytics), retornando `HttpResponse` temporários para validar a conectividade de cada endpoint.
- **Manutenibilidade**: Este esqueleto serve como a base para o desenvolvimento incremental, permitindo que cada funcionalidade seja preenchida com a lógica real de banco de dados e templates de forma isolada e segura.

<hr>

# feat(auth): implement registration and logout logic

- **`register(request)`**:
  - **POST**: Processa o `UserCreationForm`. Se válido, salva o usuário, realiza o login automático e redireciona para o `dashboard`, exibindo uma mensagem de sucesso via `django.contrib.messages`.
  - **GET**: Exibe um formulário em branco para o cadastro.
- **`logout_view(request)`**:
  - Encerra a sessão do usuário atual e redireciona para a página inicial (`index`), garantindo a limpeza dos dados de sessão no servidor.

### Observação Técnica

- **Segurança**: O uso de `UserCreationForm` (nativo do Django) é a prática recomendada, pois ele já cuida da validação de senhas, verificação de força e sanitização de dados, prevenindo vulnerabilidades comuns de injeção e manipulação de credenciais.

https://docs.djangoproject.com/en/6.0/topics/auth/default/ - UserCreationForm

<hr>

# feat(views): Implement CRUD views for Subject model

- **`subjects_list(request)`**: Lista todas as matérias associadas ao usuário logado, garantindo isolamento de dados.
- **`subject_create(request)`**: Processa a criação de uma nova matéria. Utiliza `.strip()` (serve para remover espaços em branco no início e no fim de uma string) e define um valor padrão para a cor caso não seja informada.
- **`subject_detail(request, pk)`**: Recupera uma matéria específica do usuário (`get_object_or_404`) e exibe seus tópicos relacionados.
- **`subject_edit(request, pk)`**: Realiza a edição das propriedades da matéria e persiste as alterações no banco de dados.
- **`subject_delete(request, pk)`**: Gerencia a remoção da matéria através de uma requisição `POST`, garantindo que a exclusão seja intencional.

### Observações Técnicas

- **Segurança (Data Isolation)**: Todas as queries filtram pelo `user=request.user`. Isso é crucial para que um usuário não consiga acessar ou manipular matérias de outro usuário ao manipular o ID (`pk`) na URL.
- **User Experience (UX)**: A utilização do `messages` fornece confirmação visual ao usuário após cada ação (criação, edição ou deleção), elevando a usabilidade da aplicação.
- **`get_object_or_404`**: Esta função é um atalho profissional do Django que retorna automaticamente uma página de erro 404 caso o objeto não exista ou não pertença ao usuário, evitando erros de servidor (`DoesNotExist`).

<hr>

# feat(views): Implement CRUD views for Topic model

- **`topic_create(request)`**:
  - Utiliza o decorador `@require_POST` para garantir que a criação ocorra apenas via envio de formulário.
  - Valida a existência da matéria antes da criação, garantindo que o tópico seja vinculado corretamente ao usuário autenticado.
- **`topic_toggle(request, pk)`**:
  - Endpoint assíncrono (API) para alternar o status `is_completed`.
  - Retorna um JSON contendo o novo estado e o percentual de progresso atualizado da matéria, permitindo atualização instantânea do front-end sem recarregar a página.
- **`topic_delete(request, pk)`**:
  - Remove o tópico e retorna um JSON com a confirmação de exclusão e o novo progresso da matéria pai.

### Observações Técnicas

- **Consistência de Dados**: Ao retornar o `progress()` dentro das respostas JSON de `toggle` e `delete`, você possibilita que a interface (dashboard ou página de detalhes) reflita o progresso real em tempo real sempre que uma interação ocorre.
- **Segurança**: O filtro `subject__user=request.user` garante que, mesmo em uma API, um usuário só consiga manipular tópicos que pertencem às suas próprias matérias.

<hr>

# feat(views): implement Pomodoro session management

- **`pomodoro(request)`**:
  - Renderiza o timer.
  - Carrega a lista de matérias (`subjects`) para o usuário associar o tempo de estudo.
  - Busca as últimas 10 sessões concluídas (`recent`) para exibir um histórico rápido de produtividade.
- **`pomodoro_save(request)`**:
  - Processa o JSON enviado pelo timer ao finalizar a contagem.
  - Persiste a instância de `PomodoroSession` vinculando-a ao usuário e à matéria selecionada.

### Observações Técnicas

- **`json.loads(request.body)`**: Como o Pomodoro é um timer que roda no cliente (JavaScript), o `pomodoro_save` espera um `POST` contendo dados estruturados em JSON em vez de um formulário padrão. Isso oferece maior flexibilidade para o seu front-end.
- **Data/Hora**: A utilização de `datetime.now()` registra o momento exato da finalização (ou salvamento) no servidor. Dependendo do seu deploy, considere utilizar `django.utils.timezone.now()` para manter a consistência de fusos horários globalmente.
- **Segurança**: Assim como nas outras rotas, a validação `user=request.user` garante que apenas sessões legítimas sejam criadas, protegendo seus dados de Analytics contra requisições maliciosas.

<hr>

# feat(views): Implement WeeklyGoal CRUD operations

* **`goals_list(request)`**:
* Calcula dinamicamente a data de início da semana (segunda-feira) utilizando `date.today()` e `weekday()`.
* Exibe apenas as metas pertinentes à semana corrente, garantindo que o usuário visualize sempre o progresso atual.


* **`goal_create(request)`**:
* Utiliza `update_or_create` para gerenciar as metas. Isso é fundamental para evitar a duplicação de dados, permitindo que o usuário altere a meta de uma matéria na mesma semana sem criar registros conflitantes.
* Assegura que a meta esteja vinculada estritamente às matérias do usuário logado.


* **`goal_delete(request, pk)`**:
* Permite a remoção de metas registradas, protegendo a operação com o filtro de propriedade do usuário.

### Observações Técnicas

* **Lógica de Calendário**: A subtração `today - timedelta(days=today.weekday())` é a maneira mais eficiente em Python puro para normalizar qualquer data para a segunda-feira daquela semana. Isso padroniza o seu banco de dados, facilitando queries futuras.
* **Idempotência**: O uso de `update_or_create` torna a aplicação muito mais robusta. O usuário não precisa se preocupar se ele já criou a meta antes; o sistema apenas atualiza o valor da meta de horas caso ela já exista para aquela semana.

<hr>

# feat(views): Implement dashboard and activity analytics views

* **`dashboard(request)`**:
* Centraliza a inteligência do sistema: calcula o total de flashcards pendentes de revisão, horas de estudo na semana atual, progresso em metas semanais (`WeeklyGoal`) e o cálculo de *streak* (dias consecutivos de estudo).
* Prepara o contexto completo para a home page do usuário com métricas de produtividade.


* **`dashboard_activity(request)`**:
* Endpoint de API focado em analytics: agrupa o número de sessões Pomodoro concluídas nos últimos 12 meses (agrupadas por dia).
* Retorna um `JsonResponse` formatado para consumo por bibliotecas de gráficos (como Chart.js ou D3.js).


---

### Observações Técnicas

* **Cálculo de Streak**: A implementação utiliza um loop `while` reverso (`check_date -= timedelta(days=1)`), que é uma forma eficiente de verificar a continuidade do estudo sem precisar processar todo o histórico do banco de dados de uma vez.
* **Agregação de Dados**: No `dashboard_activity`, a utilização de `.values("started_at__date")` otimiza a consulta ao banco, extraindo apenas a informação necessária para o processamento do dicionário de contagens.
* **Performance**: O uso de métodos como `count()` e a filtragem inteligente garantem que o dashboard carregue métricas pesadas de forma rápida, mesmo com o aumento do volume de dados do usuário.

<hr>

# fix(views): enforce authentication and HTTP method constraints

* **Segurança de Acesso (`@login_required`)**:
* Aplicado às views de gerenciamento (Subjects, Goals, Dashboard, etc.) para garantir que usuários não autenticados sejam redirecionados para a tela de login.


* **Integridade de Ação (`@require_POST`)**:
* Reforçado nos métodos que alteram estado no banco de dados (`create`, `edit`, `delete`, `save`), evitando que ações destrutivas ou de escrita sejam executadas via requisições `GET` acidentais (ex: busca de robôs ou erro de digitação de URL).


---

### Observação Técnica

* **Proteção contra CSRF**: Ao combinar `@require_POST` com os formulários do Django (que utilizam a tag `{% csrf_token %}`), é criado uma camada de segurança robusta contra ataques de *Cross-Site Request Forgery*.

<hr>

# feat(templates) - Implement base layout with navigation and global messaging

* **Estrutura (`base.html`)**: Implementação do template mestre utilizando o sistema de herança do Django (`{% block content %}`).
* **Componentes Globais**:
* **Navegação (Navbar)**: Menu de navegação responsivo (Bootstrap 5) com links para todos os módulos (Dashboard, Matérias, Flashcards, Pomodoro, Metas) e botão de Logout, condicionado ao estado de autenticação (`user.is_authenticated`).
* **Sistema de Mensagens**: Integração automática do `django.contrib.messages` exibindo alertas dinâmicos (sucesso, erro, aviso) que aparecem antes de cada `block content`, proporcionando feedback imediato ao usuário.


* **Ativos**:
* Integração com **Bootstrap 5** (CSS/JS) para o grid e componentes.
* Integração com **Bootstrap Icons** para identidade visual dos módulos.
* Configuração de link para arquivo CSS estático personalizado (`{% static 'css/styles.css' %}`).



---

### Observação Técnica

* **Herança de Blocos**: A estrutura utiliza `{% block title %}`, `{% block content %}` e `{% block scripts %}`, permitindo que páginas filhas injetem conteúdo específico sem a necessidade de reescrever o layout da navbar ou scripts de carregamento global.
* **UX/UI**: A utilização do formulário `POST` para o `logout` respeita a segurança do Django contra CSRF, garantindo que o encerramento da sessão não ocorra por erro ou indexação indevida.
* **Bootstrap**: A escolha pelo Bootstrap 5 garante um layout profissional e *mobile-first* com esforço mínimo de CSS customizado, ideal para um MVP de Capstone.

<hr>

# feat(frontend): implement activity heatmap rendering script

* **Fetch API**: Realiza uma requisição assíncrona ao endpoint `/dashboard/activity/` para recuperar o dicionário de contagem de sessões dos últimos 12 semanas.
* **Geração Dinâmica (`HTML Grid`)**: Itera retroativamente pelos últimos 84 dias (12 semanas $\times$ 7 dias), formatando a data no padrão ISO `YYYY-MM-DD` para corresponder às chaves retornadas pela API.
* **Mapeamento de Cores (Intensidade)**:
* `0 sessões`: `#ebedf0` (vazio/cinza claro)
* `1 sessão`: `#9be9a8` (verde claro)
* `2 sessões`: `#40c463` (verde médio)
* `>= 3 sessões`: `#216e39` (verde escuro)


* **Legenda e Tooltips**: Adiciona atributos `title` nativos para exibir o detalhamento de data e quantidade por quadradinho, acompanhado de uma legenda textual indicando a escala de atividade ("menos" a "mais").

---

### Observação Técnica

* **GitHub-style Contribution Grid**: Essa implementação replica o design visual dos gráficos de contribuição do GitHub no front-end utilizando divs com flexbox, consumindo diretamente o JSON gerado pela view `dashboard_activity` que criamos anteriormente.

<hr>

# feat(templates): implement user dashboard template with analytics and overview cards

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) sobrescrevendo os blocos de título (`title`), conteúdo (`content`) e scripts (`scripts`).
* **Cards de Resumo**: Exibição em grid (Bootstrap 5) dos contadores principais (`total_subjects`, `total_flashcards`, `week_hours` e contagem de `streak`).
* **Alertas e Metas**: Alerta condicional para flashcards pendentes de revisão (`due_cards`) e barras de progresso dinâmicas baseadas nas cores e horas cumpridas de cada `WeeklyGoal`.
* **Histórico e Heatmap**: Listagem de sessões recentes de estudo e carregamento do container do heatmap de atividades através do script customizado `dashboard.js`.

<hr>

# feat(templates): implement user registration template with auth card layout

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) definindo o título "Cadastrar".
* **Card de Autenticação**: Estrutura de formulário encapsulada em um container centralizado (`auth-card`).
* **Segurança de Formulário**: Injeção obrigatória do token de proteção contra falsificação de requisições (`{% csrf_token %}`) e renderização automática dos campos via `{{ form.as_p }}`.
* **Navegação Auxiliar**: Link de redirecionamento integrado para usuários que já possuem cadastro na plataforma (`login`).

<hr>

# feat(templates): implement user login template with auth card layout

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) definindo o título "Entrar".
* **Card de Autenticação**: Estrutura de formulário encapsulada em um container centralizado (`auth-card`) mantendo a coerência visual com a página de cadastro.
* **Segurança de Formulário**: Injeção obrigatória do token de proteção contra falsificação de requisições (`{% csrf_token %}`) e renderização automática dos campos via `{{ form.as_p }}` do Django.
* **Navegação Auxiliar**: Link de redirecionamento integrado para usuários que ainda não possuem cadastro na plataforma (`register`).

<hr>

# fix(config): configure static files and authentication redirect paths

* **Configuração de Arquivos Estáticos**: Adicionou `STATIC_URL` e `STATIC_ROOT` utilizando `BASE_DIR / 'staticfiles'`, preparando o projeto para coletar e servir arquivos estáticos de forma correta (essencial para ambientes de produção ou coleta com `collectstatic`).
* **Rotas de Autenticação Globais**: Definidas as constantes `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL` para direcionar o fluxo de sessões do usuário de forma automatizada pelo Django.
* **Roteamento Raiz (`urls.py`)**: Inclusão de `path('', include('core.urls'))` no arquivo principal de URLs do projeto, conectando o roteador central diretamente às rotas da aplicação `core`.

---

### Observação Técnica

* **`STATIC_ROOT`**: Especifica o diretório absoluto onde o comando `collectstatic` reunirá todos os arquivos estáticos da aplicação para servi-los eficientemente em produção.
* **Fluxo de Redirecionamento**: Configurar `LOGIN_REDIRECT_URL = "/"` e `LOGOUT_REDIRECT_URL = "/login/"` garante que o `@login_required` e os componentes de login/logout saibam exatamente para onde encaminhar o usuário após autenticar ou encerrar a sessão.

<hr>

# feat(templates): implement subjects list template with card grid and progress indicators

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) definindo o título "Subjects".
* **Cabeçalho de Ação**: Título com ícone e botão de atalho para a criação de uma nova matéria (`subject_create`).
* **Grid de Matérias (`Responsive Cards`)**: Itera sobre a lista de matérias usando um sistema de colunas adaptativo (`col-12 col-md-6 col-lg-4`). Cada card exibe:
* Indicador visual de cor dinâmico (`subject.color`).
* Descrição opcional truncada.
* Barra de progresso percentual calculada via método do modelo (`subject.progress`).
* Ações rápidas de navegação (`subject_detail`), edição (`subject_edit`) e exclusão (`subject_delete`).


* **Estado Vazio (`Empty State`)**: Exibição condicional de mensagem informativa com ícone centralizado caso o usuário não possua nenhuma matéria cadastrada.

<hr>

# feat(templates): implement subject form template for create and edit actions

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) com título dinâmico baseado na variável de ação (`{{ action }} Matéria`).
* **Estrutura de Formulário**: Layout centralizado em largura otimizada (`col-12 col-md-6`) para melhor usabilidade em telas médias e grandes.
* **Campos e Validação**:
* Campo `name` obrigatório, injetando o valor atual caso esteja em modo de edição (`{{ subject.name|default:'' }}`).
* Campo `description` em textarea opcional.
* Seletor de cor customizado (`input type="color"`) utilizando o padrão do Bootstrap (`form-control-color`) e valor padrão de fallback (`#4A90D9`).


* **Ações**: Botões de submissão para persistir dados e link de cancelamento com retorno direto para a listagem (`subjects_list`).

<hr>

# feat(templates): implement subject detail template with interactive topic list and progress sync`

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) usando o nome da matéria como título dinâmico (`{{ subject.name }}`).
* **Cabeçalho de Progresso**: Exibição da cor identificadora da matéria, título e um badge com a barra de progresso sincronizada em tempo real (`{{ subject.progress }}`).
* **Gerenciamento de Tópicos**:
* Formulário integrado para a adição rápida de novos tópicos vinculados ao ID da matéria atual (`topic_create`).
* Listagem interativa com caixas de seleção dinâmicas (`topic-toggle`) e botões de remoção (`topic-delete`).
* Aplicação condicional de classes de texto riscado (`text-decoration-line-through`) para itens concluídos.


* **Scripts e Configuração**: Injeção de variáveis globais via template tag script (`TOGGLE_URL`, `DELETE_URL`, `CSRF_TOKEN`) para consumo pelo script assíncrono `topics.js`.

<hr>

# feat(frontend): implement asynchronous topic toggle and deletion logic with progress updates`

* **Toggle de Conclusão**: Intercepta o evento `change` dos checkboxes de tópicos, disparando uma requisição assíncrona (`POST`) via Fetch API com o token CSRF adequado. Atualiza visualmente o texto do tópico (riscado/cinza) e recalcula as barras e badges de progresso da página em tempo real.
* **Exclusão de Tópicos**: Intercepta o clique nos botões de lixeira com confirmação nativa (`confirm`), disparando uma requisição `DELETE` assíncrona para o endpoint correspondente e removendo o elemento do DOM em caso de sucesso.

<hr>

# feat(templates): implement subject deletion confirmation template 

* **Extensão de Layout**: Herança do arquivo base (`{% extends "layout.html" %}`) definindo o título "Excluir Matéria".
* **Card de Alerta**: Container com borda destacada em vermelho (`border-danger`) e ícone de aviso (`bi-exclamation-triangle-fill`) para alertar o usuário sobre o risco de perda permanente de dados.
* **Mensagem de Confirmação**: Exibe o nome da matéria alvo (`{{ subject.name }}`) e avisa sobre a exclusão em cascata de elementos vinculados (tópicos, flashcards e sessões).
* **Ações**: Formulário protegido com token `{% csrf_token %}` contendo botão de confirmação destrutiva (`btn-danger`) e link de cancelamento com retorno à listagem (`subjects_list`).

<hr>

# feat(templates): implement Pomodoro timer interface with subject selector and recent session history

* **Extensão de Layout**: Herança do template base (`{% extends "layout.html" %}`) definindo o título "Pomodoro".
* **Seleção de Matéria**: Dropdown centralizado (`subject-select`) para associar a sessão de estudo a uma matéria cadastrada pelo usuário.
* **Display e Controles do Timer**:
* Visor de tempo configurado para o padrão de 25 minutos (`timer-display`).
* Indicador de estado atual (`timer-label`) e botões de ação (`Start`, `Pause`, `Reset`) com estados dinâmicos e responsivos.
* Contador de ciclos e barra de progresso em tempo real integrada.


* **Histórico Recente**: Listagem condicional das últimas sessões finalizadas (`recent`) contendo duração e data/hora formatada.
* **Configuração de Scripts**: Injeção da URL de salvamento (`SAVE_URL`) e do token CSRF global para consumo pelo script front-end `pomodoro.js`.