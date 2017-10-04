import axios from 'axios'

export default {
  host: function()
  {
    return `https://v2.pwmanager.travis.sigma.ws`
  },

  headers: function()
  {
    return {
      'X-Parse-Application-Id': 'wggesucht',
      'X-Parse-REST-API-Key': 'wggesucht',
      'Content-Type': 'application/json',
    }
  },
  config: function()
  {
    return {headers:this.headers()}
  },
  getPassword: function()
  {
    return axios.get(`${this.host()}/parse/classes/Passwords`,this.config())
  },
  addPassword: function(name,pw)
  {
    let data = {'name': name,'password': pw};
    return axios.post(`${this.host()}/parse/classes/Passwords`,data,this.config())
  },
  deletePassword: function(pw)
  {
    let id = pw.objectId;
    return axios.delete(`${this.host()}/parse/classes/Passwords/${id}`,this.config())
  },
  editPassword: function(pw)
  {
    let id = pw.objectId
    let data = {'password': pw.password}
    return axios.put(`${this.host()}/parse/classes/Passwords/${id}`,data,this.config())

  },
}
