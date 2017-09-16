<template>
  <div class="test">
  <mu-toast v-if="toasts['copy']"
      message="Password copied"
      @close="hideToast('copy')"
      @click = "hideToast('copy')"
  />
  <mu-content-block>
    <mu-row gutter>
      <mu-col width="100"/>
      <mu-col width="100">
        <mu-text-field icon="search" class="appbar-search-field" hintText="Search for Passwords"/>
      </mu-col>
      <mu-col width="100"/>
    </mu-row>
  </mu-content-block>

  <mu-content-block>
  <mu-paper>
      <mu-list>
        <password-item
          v-for="password in passwords"
          :password="password"
          @passwordClicked="copySuccessHandler"
        />
      </mu-list>
  </mu-paper>
  </mu-content-block>
  </div>
</template>

<script>
import PasswordItem from '~/components/PasswordItem.vue'
import _ from 'lodash'

export default {
  name: 'pwmanager',
  props: ['passwords'],
  data () {
    return {
      toastTimers : {},
      toasts : {
        copy: false,
      }
    }
  },
  computed: {
  },
  created() {

    this.$on('deletePassword',(pw) =>
    {
      this.passwords.push({'name':'hihi','password':'hohoho'})
    });
  },
  events: {
    passwordClicked: function(pw)
    {
      this.copyPassword(pw.pw);
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
        this.toasts[toastName] = true
        this.toastTimers[toastName] = setTimeout(() => { this.toasts[toastName] = false }, secs * 1000)
    },

    copySuccessHandler: function()
    {
      this.makeToastForNSeconds('copy',2)
    },

  },
  components: {
    'password-item': PasswordItem
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
