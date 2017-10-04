from node:latest

run git clone https://github.com/travistang/pwmanager /pwmanager
#run cd /pwmanager/pwmanager-nuxt/pwmanager && npm run dev
run cd /pwmanager/pwmanager-nuxt/pwmanager && npm install --silent

expose 3000
workdir /pwmanager/pwmanager-nuxt/pwmanager
cmd ["npm","run","deploy"]
