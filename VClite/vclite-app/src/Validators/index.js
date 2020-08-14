import { extend } from 'vee-validate';
import { setInteractionMode } from 'vee-validate';
import axios from "axios";
import { userService } from '../_services';

import { 
    email, 
    required, 
    min,
    max,
    alpha,
    password,
} from 'vee-validate/dist/rules';


setInteractionMode('lazy');


extend('email', {
    ...email,
    message: 'You should add a valid email address'
});

extend('required', {
    ...required,
    message: 'This field is required.'
});

extend('alpha', {
  ...alpha,
  message: 'Only alphabets allowed'
})

extend('minValue', {
  validate(value, {inp}) {
    return value >= inp;
  },
  params: ['inp'],
  message: 'Price can\'t be 0'
});

extend('min', {
  validate(value, { length }) {
    return value.length >= length;
  },
  params: ['length'],
  message: 'Min {length} characters required.'
});

extend('max', {
  validate(value, { length }) {
    return value.length <= length;
  },
  params: ['length'],
  message: 'Only {length} characters allowed.'
});


extend('password', {
  params: ['target'],
  validate(value, { target }) {
    return value === target;
  },
  message: 'Password confirmation does not match'
});