# pwmanager
My password manager
# Usage
1. Have the [parse-server](https://github.com/yongjhih/docker-parse-server) stack ready
2. `git clone https://github.com/travistang/pwmanager`
3. `cd pwmanager/pwmanager-nuxt`
4. `docker build -t="v2-pwmanager" .`
5. `docker run -d -p 3000:3000 --name v2-pwmanager v2-pwmanager`
