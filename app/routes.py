from app import app,db
from flask import render_template,flash,redirect,url_for,request
from flask_login import current_user,login_user,login_required,logout_user
from werkzeug.urls import url_parse
from app.forms import LoginForm,RegistrationForm,Postform,Like,RoomForm
from app.models import User,Group,Post,Comment,memb,Room

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/home' , methods=['GET', 'POST'])
@login_required
def home():
    form = Postform()
    like = Like()
    if form.validate_on_submit():
        gro = request.form['group_options']
        p = Post(body=form.body.data,author=current_user,group=Group.query.filter_by(id = int(gro))[0])
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('home'))
    if like.validate_on_submit():
        lik = request.form['Like']
        try:
            current_user.liked_posts.append(Post.query.all()[int(lik)-1])
            db.session.commit()
        except:
            return redirect(url_for('comment',id1=str(lik[2])))
    posts = []
    for group in current_user.groups:
        for post in group.posts:
            posts.append(post)
    groups = []
    for i in db.session.query(memb).filter(memb.c.user_id == current_user.id):
        if i.status == 1 or i.status==2:
            groups.append(Group.query.filter_by(id = i.group_id)[0])
    return render_template('dashboard2.html',posts=posts,user = current_user,groups = groups,form=form ,like = like)

@app.route('/comment/<string:id1>',methods=['GET', 'POST'])
@login_required
def comment(id1):
    if id1 is not None:
        form = Postform()
        post = Post.query.filter_by(id=int(id1))[0]
        if form.validate_on_submit():
            com = Comment(body=form.body.data,author=current_user,post = post)
            db.session.add(com)
            db.session.commit()
            return redirect(url_for('comment',id1=str(id1)))       
    else:
        return redirect(url_for('home'))
    return render_template('comment.html',post = post,user = current_user,form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username and Password')
            return redirect(url_for('login'))

        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, batch = form.batch.data, city = form.city.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/groups',methods=['GET','POST'])
@login_required
def groups():
    form = Like()
    if form.validate_on_submit():
        grp = request.form['groups']
        Group.query.all()[int(grp)-1].members.append(current_user)
        db.session.commit()

    groups = []

    for i in Group.query.all():
        if len(db.session.query(memb).filter(memb.c.user_id == current_user.id,memb.c.group_id == i.id).all()) == 0:
            groups.append(i)
    return render_template('groups.html',title = 'All groups',groups = groups,user= current_user,form = form)

@app.route('/notifications',methods=['GET','POST'])
@login_required
def notifications():
    form = Like()
    if form.validate_on_submit():
        g = request.form['accept']
        if int(g[1]) == 2 and g[2] == " ":
            db.session.query(memb).filter(memb.c.user_id == int(g[3]),memb.c.group_id == int(g[5])).update({"status" : memb.c.status + 1},synchronize_session=False)
            db.session.commit()
        elif int(g[1]) == 2 and g[2] == "C":
            db.session.query(memb).filter(memb.c.user_id == int(g[4]),memb.c.group_id == int(g[6])).delete(synchronize_session=False)
            db.session.commit()
        elif int(g[1]) == 1 and g[2] ==" ":
            db.session.query(Post).filter(Post.id == int(g[3])).update({"status" : Post.status + 1},synchronize_session=False)
            db.session.commit()
        else:
         db.session.query(Post).filter(Post.id == int(g[4])).delete(synchronize_session=False)
         db.session.commit()
        return redirect(url_for('notifications'))
    notif1 = []
    notif2 = []
    for i in db.session.query(memb).filter(memb.c.user_id == current_user.id).all():
        if i.status == 2:
                for post in Group.query.filter_by(id = i.group_id)[0].posts:
                    if post.status ==0:
                        notif1.append(post)
                for user in db.session.query(memb).filter(memb.c.group_id == i.group_id).all():
                    if user.status == 0:
                        notif2.append(User.query.filter_by(id = user.user_id)[0])
                        notif2.append(Group.query.filter_by(id = i.group_id)[0])
    return render_template('notifications.html',user = current_user,notif1 = notif1,notif2 = notif2,form = form)


@app.route('/roomallocation', methods=['GET', 'POST'])
@login_required
def roomalloc():
    form = RoomForm()
    if form.validate_on_submit():
        if form.check_availabity_room(form.roomno.data,current_user):
            room = Room(roomno=form.roomno.data,user_id=current_user.id)
            db.session.add(room)
            db.session.commit()
            flash('Success !! You have booked a room')
    return render_template('room.html', title='Room Allocation', form=form)
