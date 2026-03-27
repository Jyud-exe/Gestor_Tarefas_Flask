from itsdangerous import SignatureExpired, BadSignature
from flask_login import login_user, logout_user, login_required, current_user
from mod import app
from flask import render_template, redirect, url_for, request, current_app
from mod.forms import TarefasForm, LoginForm, cadForm
from mod.models import Tarefas, User
from mod import db, serializer, mail
from flask_mail import Message


@app.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    form = TarefasForm()
    hoje = form.Hoje()
    amanha = form.Amanha() 
    lista = Tarefas.query.order_by(Tarefas.time.asc()).filter_by(user_tarefa=current_user.id).all()
    if form.validate and form.is_submitted():
        print('Formulário válido, salvando tarefa!')
        form.save()
        return redirect(request.referrer)
    cadform = cadForm()
    saudacao = cadform.saudacao()
    return render_template("index.html", 
        lista=lista, 
        form=form, 
        hoje=hoje, 
        amanha=amanha,
        saudacao=saudacao)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.submit.data and form.validate_on_submit():
        autentic = User.query.get(current_user.id)
        if autentic.confirmado == False:
            token = serializer.dumps(autentic.id, salt='confirmar_email')
            link = url_for('confirmar_email', token=token, _external=True)
            msg = Message(
                subject='Confirme seu E-mail!',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[autentic.email]
            )
            msg.body=f'''Olá, {current_user.nome}

            Para finalizar seu cadastro e ter acesso completo à sua conta, basta clicar no link abaixo:

            {link}

            Se você não recebeu o link anteriormente ou ele expirou, este é o novo link válido para confirmação.

            Caso não tenha solicitado este cadastro, desconsidere este e-mail.

            Atenciosamente,
            Equipe de Suporte'''
            mail.send(msg)
            return redirect(url_for('verificacao'))
        else:
            return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    cadform = cadForm()
    if cadform.validate_on_submit():
        cadform.save()
        autentic = User.query.get(current_user.id)
        if autentic.confirmado == False:
            token = serializer.dumps(autentic.id, salt='confirmar_email')
            link = url_for('confirmar_email', token=token, _external=True)
            msg = Message(
                subject='Confirme seu E-mail!',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[autentic.email]
            )
            msg.body=f'''Olá, {current_user.nome}

            Para finalizar seu cadastro e ter acesso completo à sua conta, basta clicar no link abaixo:

            {link}

            Se você não recebeu o link anteriormente ou ele expirou, este é o novo link válido para confirmação.

            Caso não tenha solicitado este cadastro, desconsidere este e-mail.

            Atenciosamente,
            Equipe de Suporte'''
            mail.send(msg)
        return redirect(url_for('verificacao'))
    return render_template('cadastro.html', cadform=cadform)


@app.route('/confirmar_email/<token>')
def confirmar_email(token):
    try:
        user = serializer.loads(token, salt='confirmar_email', max_age=1600)
    except SignatureExpired:
        return render_template('expirado.html')
    except BadSignature:
        return render_template('link_invalido.html')
    confirm = User.query.get(user)
    confirm.confirmado = True
    db.session.commit()
    return render_template('confirmacao_sucesso.html')
    

@app.route('/verificacao')
def verificacao():
    return render_template('verificacao.html')
    

@app.route('/delete/<int:id>')
def delete(id):
    tarefa = Tarefas.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
    if request.referrer:
        return redirect(request.referrer)
    return redirect(url_for('home'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    tarefa = Tarefas.query.get(id)
    if request.method == 'POST':
        tarefa.tarefa = request.form['titulo']
        tarefa.time = request.form['horario']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('editar.html', tarefa=tarefa)


@app.route('/tarefas', methods=['GET', 'POST'])
def todas_tarefas():
    form = TarefasForm()
    agrupadas = form.agrupadas()
    return render_template('tarefas.html', agrupadas=agrupadas, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

  