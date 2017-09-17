import axios from 'axios'

export default {
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
    return axios.get(`http://localhost:1337/parse/classes/Passwords`,this.config())
  },
  addPassword: function(name,pw)
  {
    let data = {'name': name,'password': pw};
    return axios.post(`http://localhost:1337/parse/classes/Passwords`,data,this.config())
  },
  deletePassword: function(pw)
  {
    let id = pw.objectId;
    return axios.delete(`http://localhost:1337/parse/classes/Passwords/${id}`,this.config())
  },
  editPassword: function(pw)
  {
    let id = pw.objectId
    let data = {'password': pw.password}
    return axios.put(`http://localhost:1337/parse/classes/Passwords/${id}`,data,this.config())
  },
}