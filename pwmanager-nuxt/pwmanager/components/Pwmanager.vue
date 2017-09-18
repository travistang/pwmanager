<template>
  <div class="test">
  <!-- Toast session -->
  <mu-toast v-if="toasts['copy']"
      message="Password copied"
      @close="hideToast('copy')"
      @click = "hideToast('copy')"
  />
  <mu-toast v-if="toasts['delete']"
      message="Password deleted"
      @close="hideToast('delete')"
      @click = "hideToast('delete')"
  />
  <mu-toast v-if="toasts['edit']"
      message="Password edited"
      @close="hideToast('edit')"
      @click = "hideToast('edit')"
  />
  <mu-toast v-if="toasts['add']"
      message="Password added"
      @close="hideToast('add')"
      @click = "hideToast('add')"
  />
  <!-- Dialog session -->
  <mu-dialog :open="popupFlag['deletePrompt']" title="Confirm" @close="toggleDialog('deletePrompt')">
    Do you really want to delete password for {{selectedPassword?selectedPassword.name:''}}?
    <mu-flat-button
      slot="actions"
      @click="toggleDialog('deletePrompt')"
      primary
      label="No"
    />
    <mu-flat-button
      slot="actions"
      primary
      @click="toggleDialog('deletePrompt'),deletePassword(selectedPassword)"
      label="Yes"
    />
  </mu-dialog>

  <password-form
    :isEdit="isEdit"
    :password="selectedPassword"
    :open="popupFlag.editPrompt"
    :onClose="() => toggleDialog('editPrompt')"
    :onAction="() => {toggleDialog('editPrompt'),isEdit?editPassword(selectedPassword):addPassword(selectedPassword)}"
    :isProposedPasswordNameValid="isProposedPasswordNameValid"
    @newPasswordName="checkProposedPassword"
  />


  <!-- Main element-->
  <!-- search field -->
  <mu-content-block>
    <mu-row gutter>
      <mu-col width="100"/>
      <mu-col width="100">
        <mu-text-field
          v-model="filterWords"
          icon="search"
          class="appbar-search-field"
          hintText="Search for Passwords"/>
      </mu-col>
      <mu-col width="100"/>
    </mu-row>
  </mu-content-block>

  <!-- Password List -->
  <mu-content-block>
  <mu-paper>
      <mu-list>
        <!-- Top most item for adding password...-->
        <mu-list-item
          @click="promptAddPassword"
          title="Add a Password"
          class="add-pw-item"
        >
          <mu-icon value="add" slot="leftAvatar"/>

        </mu-list-item>
        <password-item
          v-for="password in filteredPasswords"
          :key="password.name"
          :password="password"
          @passwordClicked="copySuccessHandler"
          @deletePassword="promptDeletePassword(password)"
          @editPassword="promptEditPassword(password)"
        />
      </mu-list>
  </mu-paper>
  </mu-content-block>
  </div>
</template>

<script>
import PasswordItem from '~/components/PasswordItem.vue'
import PasswordForm from '~/components/PasswordForm.vue'
import DatabaseBroker from '~/assets/DatabaseBroker.js'
import _ from 'lodash'
import Vue from 'vue'
export default {
  name: 'pwmanager',
  // props: ['passwords'],

  mounted: function(){
    // initial fetch of the list of passwords from the server
    this.getPassword()
  },
  data () {
    return {
      toastTimers : {},
      toasts : {
        copy: false,
        delete: false,
        edit: false,
        add: false,
      },
      popupFlag: {
        editPrompt: false,
        deletePrompt: false,
      },
      selectedPassword: {},
      isEdit: false,
      filterWords: '',
      passwords: [],
      isProposedPasswordNameValid: true
    }
  },
  watch: {
  },
  computed: {
    filteredPasswords: function()
    {
      const searchWord = this.filterWords.trim().toLowerCase()
      // if (searchWord.length == 0) return this.passwords
      return this.passwords.filter(
        (pw) => pw.name.toLowerCase().indexOf(searchWord) > -1)
    }
  },
  methods: {
    // Toast related
    hideToast: function(toastName){
        if (this.toastTimers[toastName]) clearTimeout(this.toastTimers[toastName]);
        this.toasts[toastName] = false
    },
    hideAllToast: function()
    {
      for (let t in this.toastTimer)
      {
        this.hideToast(t);
      }
    },
    makeToastForNSeconds: function(toastName,secs)
    {
        this.hideAllToast()
        this.toasts[toastName] = true
        this.toastTimers[toastName] = setTimeout(() => { this.toasts[toastName] = false }, secs * 1000)
    },

    copySuccessHandler: function()
    {
      this.makeToastForNSeconds('copy',2)
    },
    toggleDialog: function(dialogName)
    {
      this.popupFlag[dialogName] = !this.popupFlag[dialogName]

    },
    // ask for deletion
    promptDeletePassword: function(pw)
    {
      this.selectedPassword = pw;
      this.toggleDialog('deletePrompt')
    },
    // Action function
    // really delete the password
    deletePassword: function(pw)
    {
      DatabaseBroker.deletePassword(pw)
      .then((res) => {
        // remove the deleted password from array
        this.passwords = this.passwords.filter((curPw) =>
        {
            return curPw.objectId != pw.objectId;
        })
        this.makeToastForNSeconds('delete',2)
      })
      .catch((e) => {
        error({ statusCode: 404, message: 'Cannot connect to server' })
      })
    },
    getPassword: function()
    {
      DatabaseBroker.getPassword()
      .then((res) => {
        this.passwords = res.data.results
        this.filteredPasswords = res.data.results
      })
      .catch((e) => {
        this.passwords = []
        error({ statusCode: 404, message: 'Cannot connect to server' })
      })
    },
    promptEditPassword: function(pw)
    {
      this.isEdit = true
      this.selectedPassword = pw
      this.toggleDialog('editPrompt')
    },
    promptAddPassword: function(pw)
    {
      this.isEdit = false
      this.selectedPassword = {
        name: '',
        password: '',
      }
      this.toggleDialog('editPrompt')
    },
    editPassword: function(pw)
    {
      DatabaseBroker.editPassword(pw)
      .then((res) => {
        this.getPassword()

        this.makeToastForNSeconds('edit',2)
      })
      .catch((e) => {
        error({ statusCode: 404, message: 'Cannot connect to server' })
      })

    },
    addPassword: function(pw)
    {
      return DatabaseBroker.addPassword(pw.name,pw.password)
        .then((res) => {
          // the server will return objectId and createAt only, needa populate UpdateAt as well
          const data = res.data
          pw.objectId = data.objectId
          pw.createdAt = data.createdAt
          pw.updatedAt = data.createdAt

          this.passwords.push(pw)
          this.makeToastForNSeconds('add',2)
        })
        .catch((e) => {
          error({statusCode: 404, message:e})
        });

    },
    checkProposedPassword: function(newPasswordName)
    {
      // tell the form whether the given password name is used before or not
      this.isProposedPasswordNameValid =
        this.passwords.map(p => p.name).indexOf(newPasswordName) == -1
    }
  },
  created: function()
  {
    this.$on('newPasswordName',(name) => this.checkProposedPassword(name))
  },
  components: {
    'password-item': PasswordItem,
    'password-form': PasswordForm,
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.appbar-search-field{
  color: #CCC;
  margin-bottom: 0;
  /*align:center;*/
  &.focus-state {
    color: #FFF;
  }
  .mu-text-field-hint {
    color: fade(#FFF, 54%);
  }
  .mu-text-field-input {
    color: #FFF;
  }
  .mu-text-field-focus-line {
    background-color: #FFF;
  }
}

.add-pw-item {

}

</style>
