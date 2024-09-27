function Login() {
    return (
        <div>
            <article class="round">
                <div class="header center-align">
                    <h4>Log In</h4>
                </div>
                <form method="post">
                    <div class="field label border">
                        <input type="email" id="email" name="email" required />
                        <label for="email">Email address</label>
                    </div>

                    <div class="field label border">
                        <input type="password" id="password" name="password" required />
                        <label for="password">Password</label>
                    </div>

                    <button type="submit" value="Log In">Log In</button>
                </form>
            </article>
        </div>
    );
}

export default Login;
