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
