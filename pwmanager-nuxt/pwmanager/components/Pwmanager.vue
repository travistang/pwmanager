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
    :isEdit="true"
    :password="selectedPassword"
    :open="popupFlag.editPrompt"
    :onClose="() => toggleDialog('editPrompt')"
    :onAction="() => {toggleDialog('editPrompt'),editPassword(selectedPassword)}"
  />


  <!-- Main element-->
  <!-- search field -->
  <mu-content-block>
    <mu-row gutter>
      <mu-col width="100"/>
      <mu-col width="100">
        <mu-text-field icon="search" class="appbar-search-field" hintText="Search for Passwords"/>
      </mu-col>
      <mu-col width="100"/>
    </mu-row>
  </mu-content-block>

  <!-- Password List -->
  <mu-content-block>
  <mu-paper>
      <mu-list>
        <password-item
          v-for="password in passwords"
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
import _ from 'lodash'
export default {
  name: 'pwmanager',
  props: ['passwords'],
  data () {
    return {
      toastTimers : {},
      toasts : {
        copy: false,
        delete: false,
        edit: false,
      },
      popupFlag: {
        editPrompt: false,
        deletePrompt: false,
      },
      selectedPassword: {},
    }
  },
  computed: {

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
      this.$emit('deletePassword',pw)
      this.makeToastForNSeconds('delete',2)
    },
    promptEditPassword: function(pw)
    {
      this.selectedPassword = pw;
      this.toggleDialog('editPrompt')
    },
    editPassword: function(pw)
    {
      this.$emit('editPassword',pw)
      this.makeToastForNSeconds('edit',2)
    }
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

</style>
